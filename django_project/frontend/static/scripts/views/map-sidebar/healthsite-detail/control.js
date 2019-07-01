define([
    'backbone',
    'jquery',
    'static/scripts/views/map-sidebar/healthsite-detail/detail.js',
    'static/scripts/views/map-sidebar/healthsite-detail/form.js'], function (Backbone, $, Detail, Form) {
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
            this.listenTo(shared.dispatcher, 'show-locality-detail', this.showDetail);
            this.$el = $('#locality-info');
            this.$elError = $('#locality-error');
            this.$sidebar = $('#locality-info');
            this.$editButton = $('#edit-healthsite');
            this.$createButton = $('#create-healthsite');
            this.$saveButton = $('#save-healthsite');
            this.$cancelButton = $('#cancel-healthsite');
            this.$infoWrapper = $('#info-wrapper');

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
        },
        localityError: function (message) {
            this.$el.hide();
            this.$elError.show();
            this.disabled(this.$editButton);
            if (message) {
                this.$elError.find('#information').html(message)
            }
        },
        showDetail: function (osm_type, osm_id) {
            /** Showing detail with parameter as osm_type and osm_id **/
            $('.details').hide();
            this.$sidebar.show();
            this.detail.showDefaultInfo();
            this.getInfo(osm_type, osm_id);
        },
        getInfo: function (osm_type, osm_id) {
            /** get information of healthsite from osm_type and osm_id parameters **/
            var self = this;
            this.currentAPI = this.url + osm_type + '/' + osm_id;
            self.detail_info = null;
            this.localityError('Loading locality information.');
            $.ajax({
                url: this.currentAPI + "?output=geojson",
                dataType: 'json',
                success: function (data) {
                    self.detail.showInfo(osm_type, osm_id, data);
                    self.detail_info = data;
                    self.toDetailMode();
                },
                error: function (error) {
                    self.detail.showTags({});
                    if (error['status'] === 400) {

                        self.localityError(
                            'Locality is still in pending in Healthsites server..<br>' +
                            'Please check this locality in openstreetmap with this ' +
                            '<a href="' + osmAPI + '/' + osm_type + '/' + osm_id + '">link</a>')
                    } else {
                        self.localityError(
                            'Locality is not found.<br>' +
                            'Please check this locality in openstreetmap with this ' +
                            '<a href="' + osmAPI + '/' + osm_type + '/' + osm_id + '">link</a>')
                    }
                }
            });
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
            this.$el.show();
            this.$elError.hide();
        },
        toMapMode: function () {
            /** This when detail is not opened **/
            this.toDefaultMode();
            this.disabled(this.$editButton);
        },
        toDetailMode: function () {
            /** This when detail is opened **/
            this.toDefaultMode();
            this.enabled(this.$editButton);
            this.$el.find('.data').show();
            this.$el.find('.input').hide();
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
            this.toDefaultMode();
            this.$editButton.hide();
            this.$createButton.hide();
            this.$saveButton.show();
            this.$cancelButton.show();
            this.$el.find('.data').hide();
            this.$el.find('.input').show();
            this.$el.find('.tags .fa-info-circle').show();

            // hide some of section
            this.$el.find('tr').show();
            $('*[data-tag="source_html"]').closest('tr').hide();
        },
        toCreateMode: function () {
            /** This is when edit form enabled **/
            /** Asking form to render in default inputs **/
            this.$el.find('.input').remove();
            this.form.renderForm(null, this.url);
            this.toFormMode();
            $APP.trigger('locality.create');
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
            }
            this.form.renderForm(attributes, this.currentAPI);
            this.toFormMode();
            $APP.trigger('locality.edit');
        },
        toSaveMode: function () {
            /** Asking form to push the data on form **/
            var self = this;
            this.form.save(
                function (data) {
                    self.toDefaultMode();
                    self.showDetail('node', data['id']);
                }, function (error) {
                    self.localityError('Error when uploading.<br>' + error['responseText']);
                }
            );
        },
        toCancelMode: function () {
            /** Asking form to cancel the form **/
            this.toDetailMode();
            $APP.trigger('locality.cancel');
        }
    })
});

