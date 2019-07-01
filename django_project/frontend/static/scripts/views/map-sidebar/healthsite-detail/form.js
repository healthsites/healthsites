define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        initialize: function (definitions) {
            this.definitions = definitions;
            this.listenTo(shared.dispatcher, 'form:update-coordinates', this.updateCoordinates);
        },
        renderForm: function (data, APIUrl) {
            /** RENDER FORM BASED ON DATA **/
            this.APIUrl = APIUrl;
            $.each(this.definitions, function (tag, value) {
                var inputHtml = '';
                var required = value['required'];
                var options = value['options'];
                switch (value['type']) {
                    case 'integer':
                        inputHtml = '<input class="input" type="number">';
                        break;
                    case 'float':
                        inputHtml = '<input class="input" type="number" step="0.0001">';
                        break;
                    case 'boolean':
                        options = ["True", "False"];
                    case 'string':
                        inputHtml = '<input class="input" type="text">';
                        if (!options) {
                            break;
                        }
                    case 'selection':
                        inputHtml = "<select class='input'>";
                        options = options.sort();
                        if (!value['required']) {
                            inputHtml += '<option></option>';
                        }
                        $.each(options, function (index, key) {
                            inputHtml += '<option value="' + key + '">' + key + '</option>';
                        });
                        inputHtml += "</select>";
                        break;
                }
                var $element = $('*[data-tag="' + tag + '"]');
                if ($element.length > 0) {
                    $element.find('.data').after(inputHtml);
                }

                var $input = $element.find('.input');
                $input.attr('required', required);

                // assign value to form
                if (data && data[tag]) {
                    $input.val(data[tag]);
                }
            });
            this.$latInput = $('*[data-tag="latitude"] input');
            this.$lonInput = $('*[data-tag="longitude"] input');
        },
        updateCoordinates: function (payload) {
            // set new values
            this.$latInput.val(payload.latlng.lat);
            this.$lonInput.val(payload.latlng.lng);
        },
        getPayload: function () {
            var tags = {};
            $('*[data-tag]').each(function (index) {
                var key = $(this).data('tag');
                var value = $(this).find('input,select').val();
                if (value) {
                    tags[key] = value
                }
            });
            var payload = {
                'lat': parseFloat(tags['latitude']),
                'lon': parseFloat(tags['longitude'])
            };
            delete tags['latitude'];
            delete tags['longitude'];
            payload['tag'] = tags;
            return payload;
        },
        save: function (successCallback, errorCallback) {
            $.ajax({
                url: this.APIUrl,
                type: "POST",
                dataType: 'json',
                contentType: 'application/json',
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
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
                },
                data: JSON.stringify(this.getPayload())
            })
        }
    })
});

