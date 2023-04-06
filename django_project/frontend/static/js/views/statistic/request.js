define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: api + "/facilities/",
        getStatistic: function (country, successCallback, errorCallback) {
            $.ajax({
                url: this.url + 'statistic',
                dataType: 'json',
                data: {
                    country: country,
                    filters: JSON.stringify(dataFilters)
                },
                success: function (data) {
                    if (successCallback) {
                        successCallback(data);

                        // show and hide indicators
                        if (Object.keys(dataFilters).length !== 0) {
                            $('.filters-indicator').show();
                        } else {
                            $('.filters-indicator').hide();
                        }
                    }
                },
                error: function (error) {
                    if (errorCallback) {
                        errorCallback(error)
                    }
                }
            });
        },
        getCount: function (country, successCallback, errorCallback) {
            $.ajax({
                url: this.url + 'count',
                dataType: 'json',
                data: {
                    country: country,
                    filters: dataFilters
                },
                success: function (data) {
                    if (successCallback) {
                        successCallback(data);
                    }
                },
                error: function (error) {
                    if (errorCallback) {
                        errorCallback(error)
                    }
                }
            });
        }
    })
});

