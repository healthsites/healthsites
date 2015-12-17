window.LocalitySidebar = (function () {
    "use strict";
    var need_information = "needs information";
    var no_physical_address = "No Physical Address";
    var no_phone_found = "No phone found";
    var no_operation_hours_found = "No operation hours found";
    var no_url_found = "No url found";
    var no_name = "No Name";
    var is_enable = false;
    var info_fields = [];
    var edit_fields = [];
    // private variables and functions

    // constructor
    var module = function () {
        this.$sidebar = $('#sidebar-info');

        // new style
        this.$name = $('#locality-name');
        this.$nature_of_facility = $('#locality-nature-of-facility');
        this.$completenees = $('#locality-completeness');
        this.$coordinates = $('#locality-coordinates');
        this.$physical_address = $('#locality-physical-address');
        this.$phone = $('#locality-phone');
        this.$operation = $('#locality-operation');
        this.$url = $('#locality-url');
        this.$scope_of_service = $('#locality-scope-of-service');
        this.$ancilary_service = $('#locality-ancilary-service');
        this.$activities = $('#locality-activities');
        this.$inpatient_service = $('#locality-inpatient-service');
        this.$staff = $('#locality-staff');

        // form
        this.$form = $('#locality-form');
        this.$editButton = $('#edit-button');
        this.$saveButton = $('#save-button');
        this.$addButton = $('#add-button');
        this.$cancelButton = $('#cancel-button');
        this.$physical_address_input = $('#locality-physical-address-input');
        this.$name_input = $('#locality-name-input');
        this.$phone_input = $('#locality-phone-input');
        this.$operation_input = $('#locality-operation-input');
        this.$nature_of_facility_input = $('#locality-nature-of-facility-input');

        // set info field array
        info_fields.push(this.$editButton);
        info_fields.push(this.$addButton);
        info_fields.push(this.$name);
        info_fields.push(this.$physical_address);
        info_fields.push(this.$phone);
        info_fields.push(this.$operation);
        info_fields.push(this.$nature_of_facility);

        // set editfield array
        edit_fields.push(this.$saveButton);
        edit_fields.push(this.$cancelButton);
        edit_fields.push(this.$name_input);
        edit_fields.push(this.$physical_address_input);
        edit_fields.push(this.$phone_input);
        edit_fields.push(this.$operation_input);
        edit_fields.push(this.$nature_of_facility_input);

        this.setEnable(is_enable);
        this.showDefaultInfo();

        this._bindExternalEvents();
        this._bindInternalEvents();

    };

    // prototype
    module.prototype = {
        constructor: module,

        _bindInternalEvents: function () {
            var self = this;

            this.$sidebar.on('handle-xhr-error', this.handleXHRError.bind(this));

            this.$sidebar.on('get-info', this.getInfo.bind(this));
            this.$sidebar.on('show-info', this.showInfo.bind(this));
            this.$sidebar.on('show-info-adjust', this.setInfoWindowHeight.bind(this));

            this.$sidebar.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$sidebar.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$editButton.on('click', this.showEdit.bind(this));
            this.$cancelButton.on('click', this.showEdit.bind(this));
            this.$saveButton.on('click', this.sendEdit.bind(this));

            // form if submit
            var that = this;
            this.$form.submit(function (event) {
                // Stop form from submitting normally
                event.preventDefault();

                var url = that.$form.attr("action");
                var fields = that.$form.serialize() + '&uuid=' + that.locality_data.uuid;

                // Send the data using post
                var posting = $.post(url, fields);

                var sidebar = that;
                // Put the results in a div
                posting.done(function (data) {
                    sidebar.getInfo();
                });
            });
        },
        showEdit: function (evt) {
            if (is_enable) {
                if (this.$editButton.is(":visible")) {
                    for (var i = 0; i < info_fields.length; i++) {
                        info_fields[i].hide();
                    }
                    for (var i = 0; i < edit_fields.length; i++) {
                        edit_fields[i].show();
                    }
                } else {
                    for (var i = 0; i < info_fields.length; i++) {
                        info_fields[i].show();
                    }
                    for (var i = 0; i < edit_fields.length; i++) {
                        edit_fields[i].hide();
                    }
                }
            }
        },
        setEnable: function (input) {
            console.log(input);
            is_enable = input;
            if (input) {
                this.$editButton.css({'opacity': 1});
                this.$addButton.css({'opacity': 1});
            } else {
                this.$editButton.css({'opacity': 0.7});
                this.$addButton.css({'opacity': 0.7});
            }
        },
        sendEdit: function (evt, payload) {
            this.$form.submit();
        },

        handleXHRError: function (evt, payload) {
            var xhr = payload['xhr'];

            // show error notification
            if (xhr.status === 403) {
                alert('Please login before continuing!');
            } else {
                alert('Error processing XHR request!');
            }
        },

        updateCoordinates: function (evt, payload) {
            // set new values
            $('#id_lon').val(payload.latlng.lng);
            $('#id_lat').val(payload.latlng.lat);
        },

        showDefaultInfo: function (evt) {
            if (!this.$editButton.is(":visible")) {
                this.$editButton.click();
            }

            this.$name.text(no_name);
            this.$name_input.val("");

            this.$nature_of_facility.text(need_information);
            this.$completenees.attr('style', 'width:0%');
            this.$completenees.text('0% Complete');
            this.$coordinates.text('lat: ' + 'n/a' + ', long: ' + 'n/a');

            this.$physical_address.text(no_physical_address);
            this.$physical_address.val("");

            this.$phone.text(no_phone_found);
            this.$operation.text(no_operation_hours_found);
            this.$url.text(no_url_found);
            this.$url.removeAttr('href');
            this.$scope_of_service.html('');
            this.$scope_of_service.text(need_information);
            this.$ancilary_service.html('');
            this.$ancilary_service.text(need_information);
            this.$activities.html('');
            this.$activities.text(need_information);
            this.$inpatient_service.text(need_information);
            this.$staff.text(need_information);
        },

        showInfo: function (evt) {
            // reset first
            this.showDefaultInfo();
            // set disable
            if (isLoggedIn) {
                this.setEnable(true);
            }
            console.log(this.locality_data);

            this.$name.text(this.locality_data.values['name']);
            this.$name_input.val(this.locality_data.values['name']);

            this.$nature_of_facility.text(this.locality_data.values['nature_of_facility']);
            this.$nature_of_facility.val(this.locality_data.values['nature_of_facility']);

            this.$completenees.attr('style', 'width:' + this.locality_data.completeness);
            this.$completenees.text(this.locality_data.completeness + ' Complete');
            this.$coordinates.text('lat: ' + this.locality_data.geom[0] + ', long: ' + this.locality_data.geom[1]);

            this.$physical_address.text(this.locality_data.values['physical_address']);
            this.$physical_address_input.val(this.locality_data.values['physical_address']);

            this.$phone.text(this.locality_data.values['phone']);
            this.$phone_input.val(this.locality_data.values['phone']);

            this.$operation.text(this.locality_data.values['operation']);
            this.$operation_input.val(this.locality_data.values['operation']);

            if (this.locality_data.values['url']) {
                this.$url.text(this.locality_data.values['url']);
                if (!this.locality_data.values['url'].startsWith('http://')) {
                    this.locality_data.values['url'] = 'http://' + this.locality_data.values['url'];
                }
                this.$url.attr('href', this.locality_data.values['url']);
            }

            var i;
            if (this.locality_data.values['scope_of_service']) {
                var scope_of_service_html = '<ul>';
                for (i = 0; i < this.locality_data.values['scope_of_service'].length; ++i) {
                    scope_of_service_html += '<li><i class="fa fa-caret-right"></i>';
                    scope_of_service_html += this.locality_data.values['scope_of_service'][i];
                    scope_of_service_html += '</li>';
                }
                scope_of_service_html += '</ul>';
                this.$scope_of_service.text('');
                this.$scope_of_service.html(scope_of_service_html);
            }

            if (this.locality_data.values['ancilary_service']) {
                var ancilary_service_html = '<ul>';
                for (i = 0; i < this.locality_data.values['ancilary_service'].length; ++i) {
                    ancilary_service_html += '<li><i class="fa fa-caret-right"></i>';
                    ancilary_service_html += this.locality_data.values['ancilary_service'][i];
                    ancilary_service_html += '</li>';
                }
                ancilary_service_html += '</ul>';
                this.$ancilary_service.text('');
                this.$ancilary_service.html(ancilary_service_html);
            }

            if (this.locality_data.values['activities']) {
                var activities_html = '<ul>';
                for (i = 0; i < this.locality_data.values['activities'].length; ++i) {
                    activities_html += '<li><i class="fa fa-caret-right"></i>';
                    activities_html += this.locality_data.values['activities'][i];
                    activities_html += '</li>';
                }
                activities_html += '</ul>';
                this.$activities.text('');
                this.$activities.html(activities_html);
            }
            this.$inpatient_service.text(this.locality_data.values['inpatient_service']);
            this.$staff.text(this.locality_data.values['staff']);
        },

        setInfoWindowHeight: function () {
            var nlfH = this.$sidebar_footer.height() + 15;
            this.$sidebar_body.height($(window).height() - this.$sidebar_body.offset().top - nlfH);
        },

        getInfo: function (evt, payload) {
            var self = this;
            $.getJSON('/localities/' + this.locality_uuid, function (data) {
                self.locality_data = data;
                self.$sidebar.trigger('show-info');
                if (payload) {
                    var zoomto = payload.zoomto;
                } else {
                    var zoomto = false;
                }
                $APP.trigger('locality.info', {
                    'locality_uuid': self.locality_uuid,
                    'geom': data.geom,
                    'zoomto': zoomto
                });
            });
        },

        _bindExternalEvents: function () {
            var self = this;

            $APP.on('locality.map.click', function (evt, payload) {
                self.locality_uuid = payload.locality_uuid;
                self.$sidebar.trigger('get-info', {'zoomto': payload.zoomto});
            });
            $APP.on('locality.map.move', function (evt, payload) {
                self.$sidebar.trigger('update-coordinates', payload);
            });

            $APP.on('locality.show-info-adjust', function (evt, payload) {
                self.$sidebar.trigger('show-info-adjust');
            });
        }
    }

// return module
    return module;
}());
