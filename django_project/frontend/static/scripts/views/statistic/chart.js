define([
    'backbone',
    'jquery',
    'jquery-ui',
    'c3',
    'd3'], function (Backbone, $, JqueryUI, c3, d3) {
    return Backbone.View.extend({
        url: '/countries',
        chart: null,
        initialize: function (elementID, height, width) {
            this.chart = c3.generate({
                bindto: '#' + elementID,
                size: {
                    height: height
                },
                bar: {
                    width: width
                },
                data: {
                    x: 'x',
                    y: 'percent',
                    columns: [
                        //the healthsites names
                        ['x', 'Hospitals', 'Medical clinic', 'Orthopaedic clinic'],
                        //the healthsites number
                        ['number', 0, 0, 0],
                        //the healthsites percentgage
                        ['percent', 0, 0, 0]
                    ],
                    axes: {
                        number: 'y2'
                    },
                    types: {
                        percent: 'bar',
                        number: 'bar'
                    },
                    order: 'asc',
                    labels: {
                        format: {
                            number: function (v, id, i, j) {
                                return v;
                            },
                        }
                    },
                },
                axis: {
                    rotated: true,
                    x: {
                        type: 'category',

                    },
                    y: {
                        max: 1,
                        tick: {
                            values: [0, 0.5, 1],
                            format: d3.format('%,')
                        }
                    }
                },
                legend: {
                    show: false
                },
                color: {
                    pattern: ['#b6cccc', '#f89ea1']
                }
            });
        },
        update: function (number_of_data, data) {
            var xValue = ['x'];
            var numberValue = ['number'];
            var percentValue = ['percent'];
            $.each(data, function (key, value) {
                xValue.push(key);
                numberValue.push(value);
                percentValue.push(value / number_of_data);
            });
            this.chart.load({
                columns: [
                    //the healthsites names
                    xValue,
                    //the healthsites number
                    numberValue,
                    //the healthsites percentgage
                    percentValue
                ]
            });
        }
    })
});

