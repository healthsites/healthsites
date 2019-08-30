define([
    'backbone',
    'jquery',
    'static/scripts/views/map-sidebar/healthsite-detail/detail.js',
    'static/scripts/views/map-sidebar/healthsite-detail/form.js',
    'static/scripts/views/map-sidebar/healthsite-detail/request.js',
    'static/scripts/views/map-sidebar/healthsite-detail/duplication-control.js'], function (Backbone, $, Detail, Form, Request, Duplication) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        definition_url: '/api/schema/',

        // THIS DEFINITION IS OUTSIDE OF OUR MAPPING
        definitions: {
            latitude: {
                required: true,
                type: 'float',
                description: 'latitude'
            },
            longitude: {
                required: true,
                type: 'float',
                description: 'longitude'
            },
            part_time_beds: {
                required: false,
                type: 'integer',
                description: 'Indicates the number of partial beds in a hotel or hospital'
            },
            notes: {
                required: false,
                type: 'string',
                description: 'Notes hospitalisation and outpatient consultation'
            },
            tag: {
                required: false,
                type: 'string',
                description: 'Add comma separated tags'
            },
        },
        initialize: function () {
            this.listenTo(shared.dispatcher, 'show-locality-detail', this.getLocalityDetail);
            this.listenTo(shared.dispatcher, 'show-locality-review', this.getLocalityReview);
            this.$el = $('#locality-info');
            this.$elError = $('#locality-error');
            this.$sidebar = $('#locality-info');
            this.$editButton = $('#edit-healthsite');
            this.$createButton = $('#create-healthsite');
            this.$saveButton = $('#save-healthsite');
            this.$cancelButton = $('#cancel-healthsite');
            this.$infoWrapper = $('#info-wrapper');
            this.$discardReview = $('#discard-review');
            this.$reviewError = $('#review-error');
            this.$goToForm = this.$elError.find('button');
            this.request = new Request();

            // init event
            var self = this;
            this.$editButton.click(function () {
                if (!self.isDisabled($(this))) {
                    self.toEditMode();
                }
            });
            this.$createButton.click(function () {
                if (!self.isDisabled($(this))) {
                    self.toCreateMode();
                }
            });
            this.$saveButton.click(function () {
                if (!self.isDisabled($(this))) {
                    self.toSaveMode();
                }
            });
            this.$cancelButton.click(function () {
                if (!self.isDisabled($(this))) {
                    self.toCancelMode();
                }
            });
            this.$goToForm.click(function () {
                self.$elError.hide();
                self.$el.show();
            });
            this.$discardReview.click(function () {
                $.ajax({
                    url: self.reviewAPI + "?output=geojson",
                    type: 'DELETE',
                    success: function (data) {
                        window.location = $('.profile .name a').attr('href');
                    },
                    error: function (error) {
                        self.localityError(
                            'This reviewed healthsite can\'t be deleted.<br>');
                    },
                    beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });
            });

            // GET DEFINITONS
            $.each(schema['facilities']['create']['fields'], function (index, value) {
                if (value['tags']) {
                    $.each(value['tags'], function (index, value) {
                        self.definitions[value['name']] = value;
                    })
                }
            });

            // detail and form view
            this.toMapMode();
            this.detail = new Detail(self.definitions);
            this.form = new Form(self.definitions);
            this.checkLatestUI();
            this.duplication = new Duplication();
        },
        checkLatestUI: function () {
            this.$latestUI = $('.details:visible');
        },
        localityError: function (message) {
            this.$el.hide();
            this.$elError.show();
            this.disabled(this.$editButton);
            if (message) {
                this.$elError.find('#information').html(message)
            }
        },
        showDetail: function () {
            /** Showing detail with parameter as osm_type and osm_id **/
            // TODO : remove below
            this.disabled(this.$editButton);

            $('.details').hide();
            this.$sidebar.show();
            this.detail.showDefaultInfo();
        },
        getLocalityDetail: function (osm_type, osm_id) {
            /** get information of healthsite from osm_type and osm_id parameters **/
            var self = this;
            this.showDetail();
            this.currentAPI = this.url + osm_type + '/' + osm_id;
            this.isReview = false;
            self.detail_info = null;
            this.localityError('Loading locality information.');
            this.request.getHealthsite(osm_id, osm_type,
                function (data) {
                    shared.dispatcher.trigger('locality.cancel');
                    self.$latestUI = self.$el;
                    self.detail.showInfo(osm_type, osm_id, data);
                    self.detail_info = data;
                    self.toDetailMode();
                    self.enabled(self.$editButton);
                }, function (error) {
                    self.detail.showTags({});
                    if (error['status'] === 400) {
                        shared.dispatcher.trigger('locality.cancel');
                        self.localityError(
                            'Locality is still in pending in Healthsites server for 2-5 minutes.<br>' +
                            'Please wait or please check this locality in openstreetmap by click this ' +
                            '<a href="' + osmAPI + '/' + osm_type + '/' + osm_id + '">link</a>')
                    } else {
                        self.localityError(
                            'Healthsite is not found.<br>' +
                            'Please check this healthsite in openstreetmap with this ' +
                            '<a href="' + osmAPI + '/' + osm_type + '/' + osm_id + '">link</a>')
                    }
                })
        },
        getDataFromPayload: function (payload) {
            return {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        payload['lon'],
                        payload['lat']
                    ]
                },
                "properties": {
                    "centroid": {
                        "type": "Point",
                        "coordinates": [
                            payload['lon'],
                            payload['lat']
                        ]
                    },
                    "attributes": payload['tag'],
                    "osm_id": payload['id'],
                    "osm_type": payload['type']
                }
            };

        },
        handleDuplicationFromPayload: function (data, review_id, osm_type, reason) {
            /** Handle duplication from reason **/
            osm_type = 'node';
            var self = this;
            var records = JSON.parse(reason.split('Records = ')[1]);
            data = self.getDataFromPayload(data);
            if (records.length === 1) {
                self.request.getHealthsite(records[0], osm_type,
                    function (originalData) {
                        self.duplication.showDuplication(
                            originalData, data, function (data, osm_id, mode) {
                                if (osm_id) {
                                    self.currentAPI = self.url + 'node/' + osm_id;
                                } else {
                                    self.currentAPI = self.url;
                                }
                                var params = [];
                                if (review_id) {
                                    params.push("review=" + review_id);
                                }
                                if (mode === "Yes add this") {
                                    params.push("duplication-check=false");
                                }
                                self.currentAPI += "?" + params.join("&");
                                self.detail.showInfo(osm_type, osm_id, data);
                                self.detail_info = data;
                                self.toDetailMode();
                                self.enabled(self.$editButton);
                                self.$editButton.click();
                                self.$reviewError.show();
                                if (mode === "Yes add this") {
                                    self.toSaveMode();
                                }
                            });
                    }, function (error) {
                        self.duplication.showDuplication(null, data);
                    })
            } else {
                self.duplication.duplicationMoreThanOne();
            }
        },
        getLocalityReview: function (review_id) {
            /** get information of healthsite review id **/
            var self = this;
            this.showDetail();
            this.reviewAPI = '/api/v2/pending/reviews/' + review_id;
            this.isReview = true;
            self.detail_info = null;
            this.localityError('Loading locality information.');
            this.request.getReview(review_id,
                function (data) {
                    shared.dispatcher.trigger('locality.cancel');
                    self.$latestUI = self.$el;
                    var properties = data['payload'];
                    var osm_type = properties['type'];
                    var osm_id = properties['id'];
                    var reviewReason = data["reason"];

                    var reason = "Error when create this.";
                    self.currentAPI = self.url;
                    if (osm_type && osm_id) {
                        self.currentAPI = self.url + osm_type + '/' + osm_id;
                        reason = "Error when updating this <a href='/map#!/locality/" + osm_type + '/' + osm_id + "'>location</a>.";
                    }

                    // for handle duplication
                    if (reviewReason.indexOf("Duplication") >= 0) {
                        self.handleDuplicationFromPayload(data['payload'], review_id, osm_type, reviewReason);
                    } else {
                        self.currentAPI += "?review=" + review_id;
                        self.$reviewError.html(reason + "<br>Reason = " + reviewReason);
                        data = self.getDataFromPayload(data['payload']);
                        self.detail.showInfo(data['properties']['osm_type'], data['properties']['osm_id'], data);
                        self.detail_info = data;
                        self.toDetailMode();
                        self.enabled(self.$editButton);
                        self.$editButton.click();
                        self.$reviewError.show();
                    }
                }, function (error) {
                    self.localityError(
                        'This reviewed healthsite is not found.<br>');
                    self.detail.showTags({});
                })
        },
        isDisabled: function ($button) {
            return $button.hasClass('disabled');
        },
        disabled: function ($button) {
            $button.addClass('disabled');
        },
        enabled: function ($button) {
            $button.removeClass('disabled');
        },
        toDefaultMode: function () {
            /** This is when edit and create button is show **/
            /** When detail is not opened or when detail is opened **/
            this.$editButton.show();
            this.$createButton.show();
            this.$saveButton.hide();
            this.$cancelButton.hide();
            this.$discardReview.hide();
            this.$el.show();
            this.$elError.hide();
            this.$goToForm.hide();
            this.$reviewError.hide();
        },
        toMapMode: function () {
            /** This when detail is not opened **/
            this.toDefaultMode();
            this.disabled(this.$editButton);
        },
        toDetailMode: function () {
            /** This when detail is opened **/
            this.toDefaultMode();
            // TODO : this.enabled(this.$editButton);
            this.$el.find('.data').show();
            this.$el.find('.input,.unreplaced-input').hide();
            this.$el.find('tr').show();
            this.$el.find('tr[data-hasvalue="false"]').hide();
            this.$el.find('tr[data-required="true"]').show();
            this.$el.find('.tags .fa-info-circle').hide();
            if (this.detail_info) {
                this.$infoWrapper.show();
            } else {
                this.localityError();
            }
        },
        toFormMode: function () {
            /** This is when form show **/
            $("#locality-statistic").hide();
            $("#locality-default").hide();

            this.toDefaultMode();
            this.$editButton.hide();
            this.$createButton.hide();
            this.enabled(this.$saveButton);
            this.$saveButton.show();
            if (this.isReview) {
                this.$discardReview.show();
            } else {
                this.$cancelButton.show();
            }
            this.$el.find('.data').hide();
            this.$el.find('.input,.unreplaced-input').show();
            this.$el.find('.tags .fa-info-circle').show();

            // hide some of section
            this.$el.find('tr').show();
            $('*[data-tag="source_html"]').closest('tr').hide();
        },
        toCreateMode: function () {
            /** This is when edit form enabled **/
            /** Asking form to render in default inputs **/
            this.detail.showTags({});
            this.$el.find('.input').remove();
            this.form.renderForm(null, this.url);
            this.toFormMode();
            shared.dispatcher.trigger('locality.create');
            this.$infoWrapper.hide();
        },
        toEditMode: function () {
            /** This is when edit form enabled **/
            /** Giving form current data, as default data on inputs **/
            this.$el.find('.input').remove();
            var attributes = {};
            if (this.detail_info) {
                attributes = this.detail_info['properties']['attributes'];
                if (this.detail_info['properties']['centroid']) {
                    var coordinates = this.detail_info['properties']['centroid']['coordinates'];
                    attributes['latitude'] = coordinates[1];
                    attributes['longitude'] = coordinates[0];
                }

                if (this.detail_info['properties']['osm_type'] === 'node') {
                    shared.dispatcher.trigger('locality.edit');
                }
            }
            this.form.renderForm(attributes, this.currentAPI);
            this.toFormMode();
        },
        toSaveMode: function () {
            /** Asking form to push the data on form **/
            var self = this;
            this.disabled(this.$saveButton);
            this.form.save(
                function (data) {
                    self.isReview = false;
                    self.toDefaultMode();
                    self.getLocalityDetail(self.detail_info['properties']['osm_type'], data['id']);
                    self.enabled(self.$saveButton);
                }, function (error) {
                    self.isReview = false;
                    var error = JSON.parse(error['responseText']);
                    if (error['error'].indexOf("Duplication") >= 0) {
                        var reviewID = null;
                        if (self.currentAPI.split('review=')[1]) {
                            reviewID = self.currentAPI.split('review=')[1].split('&')[0]
                        }

                        self.handleDuplicationFromPayload(error['payload'], reviewID, 'node', error['error']);
                    } else {
                        self.localityError('Error when uploading. ' + error['error']);
                        self.$goToForm.show();
                    }
                    self.enabled(self.$saveButton);
                }
            );
        },
        toCancelMode: function () {
            /** Asking form to cancel the form **/
            this.toDetailMode();
            shared.dispatcher.trigger('locality.cancel');
            if (this.$latestUI !== this.$el) {
                this.$latestUI.show();
                this.$el.hide();
                this.$elError.hide();
            } else {
                this.enabled(this.$editButton);
            }
        }
    })
});

