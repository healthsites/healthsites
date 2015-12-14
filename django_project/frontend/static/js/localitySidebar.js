window.LocalitySidebar = (function () {
    "use strict";
    var need_information = "needs information";
    var no_physical_address = "No Physical Address";
    var no_phone_found = "No phone found";
    var no_operation_hours_found = "No operation hours found";
    var no_url_found = "No url found";
    var no_name = "No Name";
    // private variables and functions

    // constructor
    var module = function () {

        this.$sidebar = $('#sidebar-info');
        this.$sidebar_head = this.$sidebar.find('.sidebar-info-header');
        this.$sidebar_body = this.$sidebar.find('.sidebar-info-body');
        this.$sidebar_footer = this.$sidebar.find('.sidebar-info-footer');

        // new style
        this.$name = $('#locality-name');
        this.$nature_of_facility = $('#locality-nature-of-facility');
        this.$completenees = $('#locality-completeness');
        this.$coordinates = $('#locality-coordinates');
        this.$physical_address = $('#locality-physical_address');
        this.$phone = $('#locality-phone');
        this.$operation = $('#locality-operation');
        this.$url = $('#locality-url');
        this.$scope_of_service = $('#locality-scope-of-service');
        this.$ancilary_service = $('#locality-ancilary-service');
        this.$activities = $('#locality-activities');
        this.$inpatient_service = $('#locality-inpatient-service');
        this.$staff = $('#locality-staff');

        this.$uploader = $('#uploader');
        this.$lastupdate = $('#last_update');

        this.showDefaultInfo();

        this._bindExternalEvents();
        this._bindInternalEvents();

    };

    // prototype
    module.prototype = {
        constructor: module,
        template: [
            '<div class="sidebar-info-header"></div>',
            '<div class="sidebar-info-body">Click a marker on the map to load locality info</div>',
            '<div class="sidebar-info-footer"></div>',
        ].join(''),

        _bindInternalEvents: function () {
            var self = this;

            this.$sidebar.on('handle-xhr-error', this.handleXHRError.bind(this));

            this.$sidebar.on('get-info', this.getInfo.bind(this));
            this.$sidebar.on('show-info', this.showInfo.bind(this));
            this.$sidebar.on('show-info-adjust', this.setInfoWindowHeight.bind(this));
            this.$sidebar.on('show-edit', this.showEdit.bind(this));

            this.$sidebar.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$sidebar_footer.on('click', '.edit', this.showEditForm.bind(this));
            this.$sidebar_footer.on('click', '.save', this.saveForm.bind(this));
            this.$sidebar_footer.on('click', '.cancel', this.cancelEdit.bind(this));

            this.$sidebar_footer.on('click', '.nl-execute', function () {
                var val = $('#nl-form-1').val();
                if (val === '1') {
                    self.showEditForm.call(self);
                }
                if (val === '2') {
                    var val2 = $('#nl-form-2').val();
                    if (val2 === '1') {
                        var loc = 'https://twitter.com/intent/tweet?text=See%20' + self.locality_data.values.name + '.%20Please%20validate&url=http://healthsites.io/%23!/locality/' + self.locality_uuid;
                        self.sendTweet(loc);
                    }
                }
                if (val === '3') {
                    var val2 = $('#nl-form-2').val();
                    if (val2 === '1') {
                        var loc = 'https://twitter.com/intent/tweet?text=See%20' + self.locality_data.values.name + '&url=http://healthsites.io/%23!/locality/' + self.locality_uuid;
                        self.sendTweet(loc);
                    }
                }
            });


            this.$sidebar_head.on('mouseover', '.label-status', function () {
                self.$sidebar_head.find('.modal-info-information').addClass('modal-info-expanded').animate({height: "100px"}, 500);
            });

            this.$sidebar_head.on('mouseout', '.label-status', function () {
                self.$sidebar_head.find('.modal-info-information').animate({height: "1px"}, 100).removeClass('modal-info-expanded');
            });
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

        sendTweet: function (text) {
            var windowOptions = 'scrollbars=yes,resizable=yes,toolbar=no,location=yes';
            var width = 550;
            var height = 420;
            var winHeight = screen.height;
            var winWidth = screen.width;
            var left = Math.round((winWidth / 2) - (width / 2));
            var top = 0;
            if (winHeight > height) {
                top = Math.round((winHeight / 2) - (height / 2));
            }
            window.open(text, 'intent', windowOptions + ',width=' + width + ',height=' + height + ',left=' + left + ',top=' + top);
        },

        cancelEdit: function (evt) {
            $APP.trigger('locality.cancel');
            // show data
            this.showInfo();
        },

        showDefaultInfo: function (evt) {
            this.$name.text(no_name);
            this.$nature_of_facility.text(need_information);
            this.$completenees.attr('style', 'width:0%');
            this.$completenees.text('0% Complete');
            this.$coordinates.text(
                'lat: ' + 'n/a' + ', long: ' + 'n/a');
            this.$physical_address.text(no_physical_address);
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
            this.$lastupdate.text("11 may 2015 17:23:15");
            this.$uploader.text("@sharehealthdata");
            this.$uploader.attr("href", "profile/sharehealthdata");
        },

        showInfo: function (evt) {
            // reset first
            this.showDefaultInfo();
            console.log(this.locality_data);
            this.$name.text(this.locality_data.values['name']);
            this.$nature_of_facility.text(this.locality_data.values['nature_of_facility']);
            this.$completenees.attr('style', 'width:' + this.locality_data.completeness);
            this.$completenees.text(this.locality_data.completeness + ' Complete');
            this.$coordinates.text(
                'lat: ' + this.locality_data.geom[0] + ', long: ' + this.locality_data.geom[1]);
            this.$physical_address.text(this.locality_data.values['physical_address']);
            this.$phone.text(this.locality_data.values['phone']);
            this.$operation.text(this.locality_data.values['operation']);

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
            if (this.locality_data.updates) {
                var updates = this.locality_data.updates;
                if (updates[0]) {
                    this.$lastupdate.text(getDateString(updates[0]['last_update']));
                    this.$uploader.text("@" + updates[0]['uploader']);
                    this.$uploader.attr("href", "profile/" + updates[0]['uploader']);
                }
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

        showEdit: function (evt, payload) {
            this.$sidebar_body.html(payload.data);
            this.$sidebar_footer.html([
                '<button type="button" class="btn btn-default cancel">Cancel</button>',
                '<button type="button" class="btn btn-warning save">Save changes</button>'
            ].join(''))

            this.$sidebar_body.find('input:text').filter(function () {
                return $(this).val() == "";
            }).each(function () {
                $(this).parents('.form-group').detach().appendTo('#empty-form-tab');
            });

        },


        showEditForm: function (evt) {
            var self = this;
            $.get('/localities/' + this.locality_uuid + '/form', function (data) {
                self.$sidebar.trigger('show-edit', {'data': data});
                // show red-marker on the map
                $APP.trigger('locality.edit', {'geom': [self.locality_data.geom[1], self.locality_data.geom[0]]});
            }).fail(function (xhr, status, error) {
                self.$sidebar.trigger('handle-xhr-error', {'xhr': xhr});
            });
        },

        saveForm: function (evt) {
            var self = this;
            var form = this.$sidebar_body.find('form');
            var latlng = [$('#id_lat').val(), $('#id_lon').val()];
            var data = form.serializeArray();

            $.ajax('/localities/' + this.locality_uuid + '/form', {
                'type': 'POST',
                'data': data,
                'success': function (data, status, xhr) {
                    if (data !== 'OK') {
                        // there were some form processing errors
                        self.$sidebar.trigger('show-edit', {'data': data});
                    } else {
                        // everything went ok, get new data from the server and show info
                        self.$sidebar.trigger('get-info');

                        $APP.trigger('locality.save');
                    }
                },
                'error': function (xhr, status, error) {
                    self.$sidebar.trigger('handle-xhr-error', {'xhr': xhr});
                }
            })
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
