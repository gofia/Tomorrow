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
                    server_production[i].fields.production_oil
                ]);
                x = $.month_diff(first_date, date);
                if (x >= data.x_min) {
                    fit.push([
                        date,
                        fit_function(x)
                    ]);
//                    fit_range.push([
//                        date,
//                        fit_function(x) * (1 - data.error_std),// * (1 - data.error_avg),
//                        fit_function(x) * (1 + data.error_std)// * (1 - data.error_avg)
//                    ]);
                }
            }

            if (data.forecasts) {
                var forecasts = JSON.parse(data.forecasts),
                    forecast_avg = [],
                    forecast_range = [];
                for (i = 0; i < forecasts.length; i++) {
                    date = $.to_date(forecasts[i].date);
                    forecast_avg.push([date, forecasts[i].average]);
                    forecast_range.push([
                        date,
                        forecasts[i].average * (1 - forecasts[i].sigma),
                        forecasts[i].average * (1 + forecasts[i].sigma)
                    ]);
                    if (date >= last_date) {
                        x = $.month_diff(first_date, date);
    //                    fit.push([
    //                        date,
    //                        fit_function(x)
    //                    ]);
                        fit_range.push([
                            date,
                            fit_function(x) * (1 - data.error_std) * (1 - data.error_avg),
                            fit_function(x) * (1 + data.error_std) * (1 - data.error_avg)
                        ]);
                    }
                }
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

            var plot_options = {
                chart: {
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text: 'Production of the field ' + data.name
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' :
                        'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'datetime',
                    maxZoom: 14 * 24 * 3600000, // fourteen days
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    title: {
                        text: 'barrel/month'
                    }
                },
                tooltip: {
                    shared: true
                },
                legend: {
                    enabled: false
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
//                plot_options.series.push({
//                    type: 'line',
//                    name: 'Forecast',
//                    data: forecast_avg
//                });
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
            }

            details_box.find('.container').highcharts(plot_options);

            plot_options.series = [
                {
                    type: 'area',
                    name: 'forecast error',
                    data: sum_errors
                }
            ];
            plot_options.title.text = "Error on future total production";
            plot_options.yAxis.title.text = "%";

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
    }

    //$.getJSON("/api/countries/").done(plot);

    $.load_field_production = function (field_id, details_box) {
        $.getJSON("/api/productions/" + field_id + "/")
            .done($.plot_details(details_box));
    };
});