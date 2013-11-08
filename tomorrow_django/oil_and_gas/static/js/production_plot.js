/**
 * Created by Lucas-Fievet on 10/19/13.
 */

$(function () {

    function plot(data) {
        data = data[0];
        var server_production = JSON.parse(data.production_oil),
            productions = [],
            total_oil_production = 0,
            fit = [],
            As = [],
            taus = [],
            betas = [],
            sum_errors = [],
            fit_function = $.stretched_exponential(data.A, data.tau, data.beta),
            first_date = $.to_date(server_production[0].fields.date),
            date = first_date,
            x = 0,
            i;

        for (i = 0; i < server_production.length; i++) {
            date = $.to_date(server_production[i].fields.date);
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
            }
        }

        $(".total-oil-production").html(total_oil_production);

        for (i = 0; i < data.fits.length; i++) {
            date = $.to_date(data.fits[i].date_end);
            As.push([date, data.fits[i].A]);
            taus.push([date, data.fits[i].tau]);
            betas.push([date, data.fits[i].beta]);
            sum_errors.push([date, data.fits[i].sum_error * 100]);
        }

        As = As.slice(Math.round(As.length/3));
        taus = taus.slice(Math.round(taus.length/3));
        betas = betas.slice(Math.round(betas.length/3));
        sum_errors = sum_errors.slice(Math.round(sum_errors.length/5));

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
                }
            ]
        };

        $('#container').highcharts(plot_options);

        plot_options.series = [
            {
                type: 'area',
                name: 'forecast error',
                data: sum_errors
            }
        ];
        plot_options.title.text = "Error on future total production";
        plot_options.yAxis.title.text = "%";

        $('#sum-error').highcharts(plot_options);

        plot_options.series = [
            {
                type: 'area',
                name: 'tau',
                data: taus
            }
        ];
        plot_options.title.text = "Fitted tau over time";
        plot_options.yAxis.title.text = "tau";

        $('#tau').highcharts(plot_options);

        plot_options.series = [
            {
                type: 'area',
                name: 'beta',
                data: betas
            }
        ];
        plot_options.title.text = "Fitted beta over time";
        plot_options.yAxis.title.text = "beta";

        $('#beta').highcharts(plot_options);
    }

    $.getJSON("/api/countries/").done(plot);

    $.getJSON("/api/fields/NO").done(function (data) {
        var i;
        for (i = 0; i < data.length; i++) {
            $("<option value='" + data[i].name + "'>" + data[i].name + "</option>").appendTo($("#fields"));
        }
        $("#fields").change(function () {
            load_field_production($("#fields").val());
        });
    });

    function load_field_production(field_name) {
        $.getJSON("/api/productions/" + field_name + "/").done(plot);
    }
});