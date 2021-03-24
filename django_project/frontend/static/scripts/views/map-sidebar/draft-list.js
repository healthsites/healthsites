define([
    'backbone',
    'jquery'], function (Backbone, $, Request) {
    return Backbone.View.extend({
        APIUrl: '/api/v2/user/IrwanFathurrahman/reviews?status=DRAFT',
        initialize: function () {
            this.$elCount = $('#draft-count');
            this.getDraft()
        },
        getDraft: function () {
            let self = this;
            if (!username) {
                $('#draft-count-wrapper').hide()
            } else {
                $.ajax({
                    url: self.APIUrl,
                    type: "POST",
                    dataType: 'json',
                    contentType: 'application/json',
                    beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    success: function (data) {
                        self.$elCount.html(data.length);
                    },
                    error: function (error) {
                        self.$elCount.html('<i>error</i>');
                    },
                    data: {
                        status: 'DRAFT'
                    }
                })
            }
        }
    })
});

