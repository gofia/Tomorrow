/**
 * Created by Lucas-Fievet on 10/19/13.
 */

$(function () {

    $.getJSON("/api/fields/").done(function (data) {
        for (var i = 0; i < data.length; i++) {
            $("<option value='" + data[i].name + "'>" + data[i].name + "</option>").appendTo($("#fields"));
        }
        $("#fields").change(function () {
            load_field_production($("#fields").val());
        });
    });

    function load_field_production(field_name) {
        $.getJSON("/api/productions/" + field_name + "/").done(function (data) {
            data = data[0]
            server_production = JSON.parse(data.production_oil);
            var productions = [],
                fit = [],
                fit_function = $.stretched_exponential(data.A, data.tau, data.beta),
                first_date = $.to_date(server_production[0].fields.date),
                date = first_date,
                x = 0;
            for (var i = 0; i < server_production.length; i++) {
                date = $.to_date(server_production[i].fields.date);
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

            $('#container').highcharts({
                chart: {
                    zoomType: 'x',
                    spacingRight: 20
                },
                title: {
                    text: 'Production of the field ' + field_name
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
                        text: 'Production in BBL'
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
            });
        });
    }
});