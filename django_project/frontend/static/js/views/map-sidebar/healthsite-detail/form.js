define([
    'backbone',
    'jquery',
    'js/views/map-sidebar/healthsite-detail/form-widget/opening-hours',
    'js/views/map-sidebar/healthsite-detail/form-widget/nominatim',
    'js/views/map-sidebar/healthsite-detail/modal/changeset-comment',], function (Backbone, $, OpeningHoursWidget, Nominatim, ChangesetModal) {
    return Backbone.View.extend({
        minChangesetComment: 10, // minimum character of changeset comment
        minChangesetSource: 5, // minimum character of changeset source
        initialize: function (definitions) {
            this.definitions = definitions;
            this.listenTo(shared.dispatcher, 'form:update-coordinates', this.updateCoordinates);
            this.opening_hours = new OpeningHoursWidget();
            this.modal = new ChangesetModal();
            this.nominatim = new Nominatim();
            this.$nominatimSuggestion = $('#nominatim-suggestion');
        },
        /**
         * Get class of depend. This is for identifiying input
         * when that input is depend on another input
         * @param value = is the input tag name
         * @returns {string}
         */
        getDependantClassName: function (value) {
            if (value) {
                return 'depend-on-' + value;
            } else {
                return 'depend-on-none';
            }
        },
        /**
         * Inserting value to input element
         * @param tag = the name of tag
         * @param inputHtml = the html that created
         * @param value = the value
         * @param required = is required or not
         */
        insertIntoElement: function (tag, inputHtml, value, required) {
            /** INSERT HTML INTO FORM ELEMENT **/
            var $element = $('*[data-tag="' + tag + '"]');
            if ($element.length > 0) {
                if ($element.find('.input').length === 0) {
                    $element.find('.data').after(inputHtml);
                }
            }

            var $input = $element.find('.input');
            $input.attr('required', required);

            // assign value to form
            if (value) {
                $input.val(value);
                $input.data('value', value);
            }

            switch (tag) {
                case 'uuid':
                    $input.prop('disabled', true);
                    break;
            }
        },
        /**
         * Rendering form of data
         * @param data = data that will be show on form
         * @param APIUrl = url that used to get the data
         */
        renderForm: function (data, APIUrl) {
            /** RENDER FORM BASED ON DATA **/
            var that = this;
            this.opening_hours.toDefault();
            this.APIUrl = APIUrl;
            if (!data) {
                data = {};
            }
            $.each(this.definitions, function (tag, value) {
                var inputHtml = '';
                var required = value['required'];
                var options = value['options'];
                var options_dict = value['options_dict'];
                var $element = $('*[data-tag="' + tag + '"]');
                switch (value['type']) {
                    case 'integer':
                        inputHtml = '<input class="input" type="number">';
                        break;
                    case 'float':
                        inputHtml = '<input class="input" type="number" step="0.0001">';
                        break;
                    case 'boolean':
                        options = ['yes', 'no'];
                    case 'string':
                        inputHtml = '<input class="input" type="text" placeholder="' + value['description'] + '" title="' + value['description'] + '" >';
                        if (!options && !options_dict) {
                            break;
                        }
                    case 'selection':
                        if (options) {
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
                        }
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
                            if (data[tag]) {
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
                if ($element.length > 0 && $element.find('.unreplaced-input').length === 0) {
                    $element.find('.data').after(inputHtml);
                }

                var $input = $element.find('.input');
                $input.attr('required', required);
            });

            // put every data into form
            $.each(data, function (tag, value) {
                that.insertIntoElement(
                    tag, '<input class="input" type="text" placeholder="this is custom tag" title="this is custom tag" >', value, false);
            });
            // source
            that.insertIntoElement(
                'source', '', null, false);

            this.$latInput = $('*[data-tag="latitude"] input');
            this.$lonInput = $('*[data-tag="longitude"] input');

            if (this.$latInput.val() && this.$lonInput.val()) {
                this.updateNominatimSearch(
                    this.$latInput.val(), this.$lonInput.val());
            }
        },
        /**
         * Updating coordinates when point is moved
         * @param payload of location
         * payload =
         * {
         *      latlng :
         *      {
         *          lat:xx, lng:yy
         *      }
         * }
         */
        updateCoordinates: function (payload) {
            // set new values
            this.$latInput.val(payload.latlng.lat);
            this.$lonInput.val(payload.latlng.lng);

            // update nominatim search
            this.updateNominatimSearch(
                payload.latlng.lat, payload.latlng.lng);
        },
        /**
         * Update nominatim from new location
         * @param lat = float
         * @param lng = float
         */
        updateNominatimSearch: function (lat, lng) {
            // update nominatim search location
            let self = this;
            this.nominatim.updateLocation(
                lat, lng
            );
            this.$nominatimSuggestion.hide();
            this.nominatim.getData(
                this.nominatim.MAJOR_AND_MINOR_STREETS,
                /**This is success callback*/
                function (data) {
                    if (data['display_name'] && data['address']) {
                        $('#nominatim-suggestion-field').html(data['display_name']);

                        // the city
                        let address = data['address'];
                        let city = null;
                        city = address['city'] ? address['city'] : city;
                        city = address['village'] ? address['village'] : city;
                        city = address['state_district'] ? address['state_district'] : city;

                        // the road
                        let road = address['road'] ? address['road'] : null;

                        // the road
                        let postcode = address['postcode'] ? address['postcode'] : null;

                        self.$nominatimSuggestion.show();
                        self.$nominatimSuggestion.click(function () {
                            // when suggestion clicked, fill the form
                            if (city) {
                                $('#addr_city input').val(city)
                            }
                            if (road) {
                                $('#addr_street input').val(road)
                            }
                            if (postcode) {
                                $('#addr_postcode input').val(postcode)
                            }
                        });
                    }
                },
                /**This is error callback*/
                function () {

                },
            )

        },
        /**
         * Return value of an element
         * @param $elementTag : element input from html
         * @returns {*}
         */
        getValue: function ($elementTag) {
            /** get value of element tag **/
            var value = null;
            var $element = $elementTag.find('input,select');
            if ($element.val()) {
                value = $element.val()
            } else {
                if ($element.data('value')) {
                    value = ''
                }
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
        /**
         * Return all value of form
         * @returns {{}}
         */
        getPayload: function () {
            var tags = {};
            var that = this;
            $('*[data-tag]').each(function (index) {
                var key = $(this).data('tag');
                var value = that.getValue($(this));

                // special value
                if (key === 'opening_hours') {
                    value = that.opening_hours.getDefiningHours();
                }
                if (value != null) {
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
        /**
         * Save the form by showing modal of comment and source
         * @param successCallback = function when success
         * @param errorCallback = function when error
         */
        save: function (successCallback, errorCallback) {
            let self = this;
            this.modal.show(
                function (data) {
                    // submitted
                    let payload = Object.assign({}, self.getPayload(), data);
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
                            if (successCallback) {
                                successCallback(data);
                            }
                        },
                        error: function (error) {
                            if (errorCallback) {
                                errorCallback(error)
                            }
                        },
                        data: JSON.stringify(payload)
                    })
                }, function () {
                    // cancelled
                    shared.dispatcher.trigger('form:enable-save-button')

                })

        }
    })
});

