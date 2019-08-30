define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        initialize: function (definitions) {
            this.definitions = definitions;
            this.listenTo(shared.dispatcher, 'form:update-coordinates', this.updateCoordinates);
        },
        getDependantClassName: function (value) {
            if (value) {
                return 'depend-on-' + value;
            } else {
                return 'depend-on-none';
            }
        },
        renderForm: function (data, APIUrl) {
            /** RENDER FORM BASED ON DATA **/
            this.APIUrl = APIUrl;
            var that = this;
            $.each(this.definitions, function (tag, value) {
                var inputHtml = '';
                var required = value['required'];
                var options = value['options'];
                var $element = $('*[data-tag="' + tag + '"]');
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
                        inputHtml = '<input class="input" type="text" placeholder="' + value['description'] + '" title="' + value['description'] + '" >';
                        if (!options) {
                            break;
                        }
                    case 'selection':
                        inputHtml = "<select class='input' title='" + value['description'] + "' >";
                        options = options.sort();
                        if (!value['required']) {
                            inputHtml += '<option></option>';
                        }
                        $.each(options, function (index, key) {
                            inputHtml += '<option value="' + key + '">' + key + '</option>';
                        });
                        inputHtml += "</select>";
                        break;
                    case 'list':
                        inputHtml = "<div class='input multiselect'>";
                        var options_with_depend_on = {};
                        var parentValues = null;
                        $.each(options, function (index, key) {
                            options_with_depend_on[key] = [that.getDependantClassName()];
                        });

                        // merge options_dependent into options
                        // tell it with parent value in class
                        if (value['options_dependent']) {
                            var depend_options = value['options_dependent']['options'];
                            $.each(depend_options, function (parent_key, options_value) {
                                $.each(options_value, function (index, key) {
                                    if (!options_with_depend_on[key]) {
                                        options_with_depend_on[key] = [];
                                    }
                                    options_with_depend_on[key].push(that.getDependantClassName(parent_key))
                                });
                            });

                            var depend_on = value['options_dependent']['depend_on'];
                            var $parentElement = $('*[data-tag="' + depend_on + '"]');
                            parentValues = that.getValue($parentElement);

                            // show hide selections based on the parent value
                            $parentElement.find('input').change(function () {
                                var className = that.getDependantClassName($(this).val());
                                if ($(this).is(':checked')) {
                                    $element.find('.' + className).show();
                                } else {
                                    $element.find('.' + className).hide();
                                    $element.find('.' + className + ' input').prop('checked', false);
                                }
                            });
                        }

                        // Render options
                        var keys = Object.keys(options_with_depend_on).sort();
                        $.each(keys, function (index, key) {
                            var selected = '';
                            if (data && data[tag]) {
                                var arraySelected = data[tag];
                                if (!$.isArray(arraySelected)) {
                                    arraySelected = arraySelected.split(';');
                                }
                                $.each(arraySelected, function (dataIndex, dataValue) {
                                    if (key === dataValue) {
                                        selected = 'checked';
                                    }
                                });
                            }

                            // check if options are displaying in default
                            var style = '';
                            if (options_with_depend_on[key][0] !== that.getDependantClassName()) {
                                style = 'display:none';
                                if (parentValues) {
                                    $.each(parentValues, function (index, parentValue) {
                                        if ($.inArray(that.getDependantClassName(parentValue), options_with_depend_on[key]) >= 0) {
                                            style = '';
                                        }
                                    });

                                }
                            }

                            // Render it
                            inputHtml += '<div class="' + options_with_depend_on[key].join(' ') + '" style="' + style + '">' +
                                '<input type="checkbox" value="' + key + '" style="width: auto!important;" ' + selected + '>' +
                                '' + capitalize(key.replaceAll('_', ' ')) + '</div>';
                        });
                        inputHtml += "</div>";
                        break;
                }
                if ($element.length > 0) {
                    $element.find('.data').after(inputHtml);
                }

                var $input = $element.find('.input');
                $input.attr('required', required);

                // assign value to form
                if (data && data[tag]) {
                    $input.val(data[tag]);
                }
                if (tag === "source") {
                    $input.val("healthsites.io");
                    $input.prop('disabled', true);
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
        getValue: function ($elementTag) {
            /** get value of element tag **/
            var value = null;
            var $element = $elementTag.find('input,select');
            if ($element.val()) {
                value = $element.val()
            }
            var $inputWrapper = $($elementTag.find('.input'));
            if ($inputWrapper.hasClass('multiselect')) {
                value = [];
                $.each($inputWrapper.find("input:checked"), function () {
                    value.push($(this).val());
                });
            }
            return value;
        },
        getPayload: function () {
            var tags = {};
            var that = this;
            $('*[data-tag]').each(function (index) {
                var key = $(this).data('tag');
                var value = that.getValue($(this));
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

