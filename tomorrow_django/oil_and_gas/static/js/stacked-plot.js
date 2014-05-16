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
            future_existing.push([date, forecasts[i].average]);
        }
        for (i = 0; i < dwarfs.length; i++) {
            date = $.to_date(dwarfs[i].date);
            if (date < start_date || end_date < date) { continue; }
            future_dwarfs.push([date, dwarfs[i].average]);
        }
        for (i = 0; i < giants.length; i++) {
            date = $.to_date(giants[i].date);
            if (date < start_date || end_date < date) { continue; }
            future_giants.push([date, giants[i].average]);
        }

        container.find('.stacked-plot').highcharts({
            chart: {
                type: 'area'
            },
            title: {
                text: 'Future production extrapolation and new discoveries'
            },
            xAxis: {
                type: 'datetime',
                tickmarkPlacement: 'on',
                title: {
                    enabled: false
                }
            },
            yAxis: {
                title: {
                    text: 'barrels (million) / month'
                },
                labels: {
                    formatter: function() {
                        return this.value / 1E6;
                    }
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