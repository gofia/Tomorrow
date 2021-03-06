/**
 * Created by Lucas-Fievet on 10/19/13.
 */

$(function () {

    $.plot_details = function (details_box) {
        return function (data) {
            var server_production = JSON.parse(data.production_oil),
                productions = [],
                total_oil_production = 0,
                fit = [],
                fit_range = [],
                As = [],
                taus = [],
                betas = [],
                sum_errors = [],
                fit_function = $.stretched_exponential(data.A, data.tau, data.beta),
                first_date = $.to_date(server_production[0].fields.date),
                last_date = 0,
                date = first_date,
                x = 0,
                i;

            for (i = 0; i < server_production.length; i++) {
                date = $.to_date(server_production[i].fields.date);
                last_date = date,
                total_oil_production += server_production[i].fields.production_oil;
                productions.push([
                    date,
                    server_production[i].fields.production_oil / 30
                ]);
                x = $.month_diff(first_date, date);
                if (x >= data.x_min) {
                    fit.push([
                        date,
                        fit_function(x) / 30
                    ]);
                    fit_range.push([
                        date,
                        fit_function(x) * (1 - data.error_std) / 30,// * (1 - data.error_avg),
                        fit_function(x) * (1 + data.error_std) / 30// * (1 - data.error_avg)
                    ]);
                }
            }

            if (data.future_dwarfs && data.future_giants) {
                var dwarfs = JSON.parse(data.future_dwarfs),
                    giants = JSON.parse(data.future_giants),
                    forecasts = JSON.parse(data.forecasts),
                    forecast_avg = {},
                    forecast_range = [],
                    dates,
                    last_date = productions.last()[0], //new Date(2008, 1, 1).getTime()
                    idx;
                for (i = 0; i < forecasts.length; i++) {
                    date = $.to_date(forecasts[i].date);
                    if (date < last_date) { continue; }
                    forecast_avg[date] = forecasts[i].average;
                    forecast_range.push([
                        date,
                        forecasts[i].average * (1 - forecasts[i].sigma) / 30,
                        forecasts[i].average * (1 + forecasts[i].sigma) / 30
                    ]);
                    if (date >= new Date().getTime()) {
                        x = $.month_diff(first_date, date);
                        fit.push([
                            date,
                            fit_function(x) / 30
                        ]);
                        fit_range.push([
                            date,
                            fit_function(x) * (1 - data.error_std) * (1 - data.error_avg) / 30,
                            fit_function(x) * (1 + data.error_std) * (1 - data.error_avg) / 30
                        ]);
                    }
                }
                dates = $.map(forecast_range, function (e) { return e[0]; });
                for (i = 0; i < dwarfs.length; i++) {
                    date = $.to_date(dwarfs[i].date);
                    idx = dates.indexOf(date);
                    if (idx === -1) { continue; }
                    forecast_avg[date] += dwarfs[i].average;
                    forecast_range[idx][1] += (dwarfs[i].average - dwarfs[i].sigma) / 30;
                    forecast_range[idx][2] += (dwarfs[i].average + dwarfs[i].sigma) / 30;
                }
                for (i = 0; i < giants.length; i++) {
                    date = $.to_date(giants[i].date);
                    idx = dates.indexOf(date);
                    if (idx === -1) { continue; }
                    forecast_avg[date] += giants[i].average;
                    forecast_range[idx][1] += (giants[i].average - giants[i].sigma) / 30;
                    forecast_range[idx][2] += (giants[i].average + giants[i].sigma) / 30;
                }
                $.staked_plot(details_box, data);
                var array = [];
                for (var key in forecast_avg) {
                    array.push([parseInt(key, 10), forecast_avg[key] / 30]);
                }
                forecast_avg = array;
            }

            for (i = 0; i < data.fits.length; i++) {
                date = $.to_date(data.fits[i].date_end);
                As.push([date, data.fits[i].A]);
                taus.push([date, data.fits[i].tau]);
                betas.push([date, data.fits[i].beta]);
                if (data.fits[i].sum_error !== 0) {
                    sum_errors.push([date, data.fits[i].sum_error * 100]);
                }
            }

            As = As.slice(Math.round(As.length / 3));
            taus = taus.slice(Math.round(taus.length / 3));
            betas = betas.slice(Math.round(betas.length / 3));
            //sum_errors = sum_errors.slice(Math.round(sum_errors.length/4));

            var title = 'Production of the field ' + data.name;
            if (data.name === "NO") {
                title = "Norwegian oil production and forecast"
            }
            if (data.name === "UK") {
                title = "U.K. oil production and forecast"
            }

            var plot_options = {
                chart: {
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text: title,
                    style: {
                        fontSize: "30px"
                    }
                },
                subtitle: {
                    text: ''
                },
                xAxis: {
                    type: 'datetime',
                    maxZoom: 14 * 24 * 3600000, // fourteen days
                    title: {
                        text: null
                    },
                    labels: {
                        style: {
                            fontSize: "20px"
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'barrels/day',
                        style: {
                            fontSize: "20px"
                        }
                    },
                    labels: {
                        style: {
                            fontSize: "20px"
                        }
                    }
                },
                tooltip: {
                    shared: true
                },
                legend: {
                    itemStyle: {
                        fontSize: "14px"
                    }
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        lineWidth: 1,
                        marker: {
                            enabled: false
                        },
                        shadow: false,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        threshold: null
                    },
                    line: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                series: [
                    {
                        type: 'area',
                        name: 'Production',
                        data: productions
                    },
                    {
                        type: 'line',
                        name: 'Fit',
                        data: fit
                    },
                    {
                        name: 'Range',
                        data: fit_range,
                        type: 'arearange',
                        lineWidth: 0,
                        linkedTo: ':previous',
                        color: Highcharts.getOptions().colors[1],
                        fillOpacity: 0.3,
                        zIndex: 0
                    }
                ]
            };

            if (data.forecasts) {
                plot_options.series.push({
                    type: 'line',
                    name: 'Forecast',
                    data: forecast_avg
                });
                plot_options.series.push({
                    name: 'Range',
                    data: forecast_range,
                    type: 'arearange',
                    lineWidth: 0,
                    linkedTo: ':previous',
                    color: Highcharts.getOptions().colors[2],
                    fillOpacity: 0.5,
                    zIndex: 0
                });

                var forecast_total = $.map(
                    forecast_avg,
                    function (e) { return e[1]; }
                ).reduce(function (a, b) {
                    return a + b;
                }, 0);
                console.log("Forecast total: " + forecast_total);
                var fit_total = $.map(
                    $.grep(fit, function (e) { return e[0] > last_date; }),
                    function (e) { return e[1]; }
                ).reduce(function (a, b) {
                    return a + b;
                }, 0);
                console.log("Fit total: " + fit_total);

                var production_total = $.map(
                    $.grep(productions, function (e) { return e[0] >= last_date && e[0] <= new Date().getTime(); }),
                    function (e) { return e[1]; }
                ).reduce(function (a, b) {
                    return a + b;
                }, 0);
                console.log("Production total: " + production_total);
                var forecast_total = $.map(
                    $.grep(forecast_avg, function (e) { return e[0] >= last_date && e[0] <= new Date().getTime(); }),
                    function (e) { return e[1]; }
                ).reduce(function (a, b) {
                    return a + b;
                }, 0);
                console.log("Forecast total: " + forecast_total);
                var fit_total = $.map(
                    $.grep(fit, function (e) { return e[0] >= last_date && e[0] <= new Date().getTime(); }),
                    function (e) { return e[1]; }
                ).reduce(function (a, b) {
                    return a + b;
                }, 0);
                console.log("Fit total: " + fit_total);
            }

            details_box.find('.container').highcharts(plot_options);

            plot_options.series = [
                {
                    type: 'area',
                    name: 'Fit error',
                    data: sum_errors
                }
            ];
            plot_options.title.text = "OSEBERG - Error on future total production";
            plot_options.yAxis.title.text = "%";
            plot_options.yAxis.min = undefined;

            details_box.find('.sum-error').highcharts(plot_options);

            plot_options.series = [
                {
                    type: 'area',
                    name: 'tau',
                    data: taus
                }
            ];
            plot_options.title.text = "Fitted tau over time";
            plot_options.yAxis.title.text = "tau";

            details_box.find('.tau').highcharts(plot_options);

            plot_options.series = [
                {
                    type: 'area',
                    name: 'beta',
                    data: betas
                }
            ];
            plot_options.title.text = "Fitted beta over time";
            plot_options.yAxis.title.text = "beta";

            details_box.find('.beta').highcharts(plot_options);
        };
    };

    //$.getJSON("/api/countries/").done(plot);

    $.load_field_production = function (field_id, details_box) {
        $.getJSON("/api/productions/" + field_id + "/")
            .done($.plot_details(details_box));
    };
});