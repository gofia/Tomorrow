/**
 * Created by Lucas-Fievet on 10/19/13.
 */

(function ($) {

    $.staked_plot = function (container, data) {
        var dwarfs = JSON.parse(data.future_dwarfs),
            giants = JSON.parse(data.future_giants),
            forecasts = JSON.parse(data.forecasts),
            future_existing = [],
            future_dwarfs = [],
            future_giants = [],
            start_date = new Date().getTime(),
            end_date = 0,
            dates = [];
        for (i = 0; i < forecasts.length; i++) {
            date = $.to_date(forecasts[i].date);
            if (date < start_date) { continue; }
            dates.push(new Date(date));
            end_date = date;
            future_existing.push([date, forecasts[i].average / 30]);
        }
        for (i = 0; i < dwarfs.length; i++) {
            date = $.to_date(dwarfs[i].date);
            if (date < start_date || end_date < date) { continue; }
            future_dwarfs.push([date, dwarfs[i].average / 30]);
        }
        for (i = 0; i < giants.length; i++) {
            date = $.to_date(giants[i].date);
            if (date < start_date || end_date < date) { continue; }
            future_giants.push([date, giants[i].average / 30]);
        }

        container.find('.stacked-plot').highcharts({
            chart: {
                type: 'area'
            },
            title: {
                text: 'U.K. future production extrapolation and new discoveries',
                style: {
                    fontSize: "30px"
                }
            },
            xAxis: {
                type: 'datetime',
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                },
                labels: {
                    style: {
                        fontSize: "20px"
                    }
                }
            },
            yAxis: {
                title: {
                    text: 'barrels / days',
                    style: {
                        fontSize: "20px"
                    }
                },
                labels: {
                    formatter: function() {
                        return this.value / 1E6 + "M";
                    },
                    style: {
                        fontSize: "20px"
                    }
                }
            },
            legend: {
                itemStyle: {
                    fontSize: "14px"
                }
            },
            tooltip: {
                shared: true,
                valueSuffix: ' millions'
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: {
                        lineWidth: 1,
                        lineColor: '#666666',
                        enabled: false
                    }
                }
            },
            series: [{
                name: 'Dwarf discoveries',
                data: future_dwarfs
            }, {
                name: 'Giant discoveries',
                data: future_giants
            }, {
                name: 'Existing fields',
                data: future_existing
            }]
        });
    };

}(window.jQuery));