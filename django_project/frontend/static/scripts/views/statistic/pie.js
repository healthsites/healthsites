define([
    'backbone',
    'jquery',
    'jquery-ui',
    'c3',
    'd3'], function (Backbone, $, JqueryUI, c3, d3) {
    return Backbone.View.extend({
        url: '/countries',
        pieChart: null,
        initialize: function (elementID, height) {
            this.piechart = c3.generate({
                bindto: '#' + elementID,
                size: {
                    height: height
                },
                data: {
                    // iris data from R
                    columns: [
                        ['complete', 0],
                        ['partial', 0],
                        ['basic', 0],
                    ],
                    colors: {
                        complete: '#f89ea1',
                        partial: '#b6cccc',
                        basic: '#8698a4'
                    },
                    type: 'pie',
                    onclick: function (d, i) {
                    },
                    onmouseover: function (d, i) {
                    },
                    onmouseout: function (d, i) {
                    }
                }
            });
        },
        update: function (basic, partial, complete) {
            this.piechart.load({
                columns: [
                    ['complete', complete],
                    ['partial', partial],
                    ['basic', basic],
                ],
            });
        }
    })
});

