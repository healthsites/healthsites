window.LocalitySidebar = (function () {
    "use strict";
    var nature_options = ["", "clinic without beds", "clinic with beds", "first referral hospital", "second referral hospital or General hospital", "tertiary level including University hospital"];
    var scope_options = ["all type of services", "specialized care", "general acute care", "rehabilitation care", "old age/hospice care"];
    var ancillary_options = ["Operating theater", "laboratory", "imaging equipment", "intensive care unit", "Emergency department"];
    var activities_options = ["medicine and medical specialties", "surgery and surgical specialties", "Maternal and women health", "pediatric care", "mental health", "geriatric care", "social care"];
    var ownership_options = ["", "public", "private not for profit", "private commercial"];
    var operation_options = ["", "24/24 & 7/7", "open only during business hours", "other"];
    var need_information = "needs information";
    var no_physical_address = "No Physical Address";
    var no_phone_found = "No phone found";
    var no_operation_hours_found = "No operation hours found";
    var no_url_found = "No url found";
    var no_name = "No Name";
    var is_enable_edit = false;
    var info_fields = [];
    var edit_fields = [];
    // private variables and functions

    // constructor
    var module = function () {
        this.$sidebar = $('#sidebar-info');

        // new style
        this.$line_updates = $('#line-updates');
        this.$name = $('#locality-name');
        this.$nature_of_facility = $('#locality-nature-of-facility');
        this.$completenees = $('#locality-completeness');
        this.$coordinates = $('#locality-coordinates');
        this.$physical_address = $('#locality-physical-address');
        this.$phone = $('#locality-phone');
        this.$operation = $('#locality-operation');
        this.$url = $('#locality-url');
        this.$scope_of_service = $('#locality-scope-of-service');
        this.$ancillary_service = $('#locality-ancillary-service');
        this.$activities = $('#locality-activities');
        this.$ownership = $('#locality-ownership');
        this.$inpatient_service = $('#locality-inpatient-service');
        this.$staff = $('#locality-staff');

        // form
        this.$form = $('#locality-form');
        this.$editButton = $('#edit-button');
        this.$saveButton = $('#save-button');
        this.$createButton = $('#create-button');
        this.$addButton = $('#add-button');
        this.$cancelButton = $('#cancel-button');
        this.$physical_address_input = $('#locality-physical-address-input');
        this.$name_input = $('#locality-name-input');
        this.$phone_input = $('#locality-phone-input');
        this.$phone_input_number = $('#locality-phone-input-number');
        this.$phone_input_int = $('#locality-phone-input-int');
        this.$operation_input = $('#locality-operation-input');
        this.$operation_specify_input = $('#locality-operation-specify-input');
        this.$nature_of_facility_input = $('#locality-nature-of-facility-input');
        this.$scope_of_service_input = $('#locality-scope-of-service-input');
        this.$scope_of_service_add = $('#locality-scope-of-service-add');
        this.$ownership_input = $('#locality-ownership-input');
        this.$ancillary_service_input = $('#locality-ancillary-service-input');
        this.$ancillary_service_add = $('#locality-ancillary-service-add');
        this.$activities_input = $('#locality-activities-input');
        this.$activities_add = $('#locality-activities-add');
        this.$inpatient_service_input = $('#locality-inpatient-service-input');
        this.$inpatient_service_full_input = $('#locality-inpatient-service-full-input');
        this.$inpatient_service_part_input = $('#locality-inpatient-service-part-input');
        this.$staff_input = $('#locality-staff-input');
        this.$staff_doctor_input = $('#locality-staff-doctor-input');
        this.$staff_nurse_input = $('#locality-staff-nurse-input');
        this.$coordinates_input = $('#locality-coordinates-input');
        this.$coordinates_lat_input = $('#locality-coordinates-lat-input');
        this.$coordinates_long_input = $('#locality-coordinates-long-input');

        // create nature options
        for (var i = 0; i < nature_options.length; i++) {
            this.$nature_of_facility_input.append("<option value=\"" + nature_options[i] + "\">" + nature_options[i] + "</option>");
        }
        // create ownershipe options
        for (var i = 0; i < ownership_options.length; i++) {
            this.$ownership_input.append("<option value=\"" + ownership_options[i] + "\">" + ownership_options[i] + "</option>");
        }
        // create operations options
        for (var i = 0; i < operation_options.length; i++) {
            this.$operation_input.append("<option value=\"" + operation_options[i] + "\">" + operation_options[i] + "</option>");
        }

        // set info field array
        info_fields.push(this.$editButton);
        info_fields.push(this.$addButton);
        info_fields.push(this.$name);
        info_fields.push(this.$physical_address);
        info_fields.push(this.$phone);
        info_fields.push(this.$operation);
        info_fields.push(this.$nature_of_facility);
        info_fields.push(this.$scope_of_service);
        info_fields.push(this.$ownership);
        info_fields.push(this.$ancillary_service);
        info_fields.push(this.$activities);
        info_fields.push(this.$inpatient_service);
        info_fields.push(this.$staff);
        info_fields.push(this.$coordinates);

        // set editfield array
        edit_fields.push(this.$cancelButton);
        edit_fields.push(this.$name_input);
        edit_fields.push(this.$physical_address_input);
        edit_fields.push(this.$phone_input);
        edit_fields.push(this.$operation_input);
        edit_fields.push(this.$nature_of_facility_input);
        edit_fields.push(this.$ownership_input);
        edit_fields.push(this.$scope_of_service_input);
        edit_fields.push(this.$scope_of_service_add);
        edit_fields.push(this.$ancillary_service_input);
        edit_fields.push(this.$ancillary_service_add);
        edit_fields.push(this.$activities_input);
        edit_fields.push(this.$activities_add);
        edit_fields.push(this.$inpatient_service_input);
        edit_fields.push(this.$staff_input);
        edit_fields.push(this.$coordinates_input);

        this.setEnable(is_enable_edit);
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

            this.$sidebar.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$sidebar.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$editButton.on('click', this.showEdit.bind(this, "edit"));
            this.$saveButton.on('click', this.sendEdit.bind(this));
            this.$addButton.on('click', this.showEdit.bind(this, "create"));
            this.$createButton.on('click', this.sendCreate.bind(this));
            this.$cancelButton.on('click', this.showEdit.bind(this));

            // -------------------------------------------------------------------
            // FORM IF SUBMIT
            // -------------------------------------------------------------------
            var that = this;
            this.$form.submit(function (event) {
                var url = that.$form.attr("action");
                var fields = that.$form.serialize();
                // Stop form from submitting normally
                event.preventDefault();
                // ------------------------------------------------------------
                // PARSING FORM
                // ------------------------------------------------------------
                {
                    // GET LAT
                    var lat = that.$coordinates_lat_input.val();
                    if (lat > 180) {
                        lat = 180;
                    } else if (lat < -180) {
                        lat = -180;
                    }
                    // GET LONG
                    var long = that.$coordinates_long_input.val();
                    if (long > 180) {
                        long = 180;
                    } else if (long < -180) {
                        long = -180;
                    }

                    // GET OPERATIONS
                    var operation = that.$operation_input.val();
                    if (operation == operation_options[operation_options.length - 1]) {
                        operation = that.$operation_specify_input.val();
                    }

                    // GET SCOPE CHILD
                    var scope_inputs = that.$scope_of_service_input.find('input');
                    var scope = "";
                    for (var i = 0; i < scope_inputs.length; i++) {
                        if ($(scope_inputs[i]).prop('checked')) {
                            scope += scope_options[i] + "|";
                        }
                    }
                    if (scope == "|") {
                        scope = "";
                    }

                    // GET ANCILLARY CHILD
                    var ancillary_inputs = that.$ancillary_service_input.find('input');
                    var ancillary = "";
                    for (var i = 0; i < ancillary_inputs.length; i++) {
                        if ($(ancillary_inputs[i]).prop('checked')) {
                            ancillary += ancillary_options[i] + "|";
                        }
                    }
                    if (ancillary == "|") {
                        ancillary = "";
                    }

                    // GET ACTIVITIES CHILD
                    var activities_input = that.$activities_input.find('input');
                    var activities = "";
                    for (var i = 0; i < activities_input.length; i++) {
                        if ($(activities_input[i]).prop('checked')) {
                            activities += activities_options[i] + "|";
                        }
                    }
                    if (activities == "|") {
                        activities = "";
                    }

                    // GET INPATIENT CHILD
                    var inpatient = that.$inpatient_service_full_input.val() + "|" + that.$inpatient_service_part_input.val();
                    if (inpatient == "|") {
                        inpatient = "";
                    }

                    // GET STAFFS CHILD
                    var staffs = that.$staff_doctor_input.val() + "|" + that.$staff_nurse_input.val();
                    if (staffs == "|") {
                        staffs = "";
                    }

                    // GET PHONE
                    var phone = "+" + that.$phone_input_int.val() + "-" + that.$phone_input_number.val();

                    if (that.locality_data != null) {
                        fields += '&uuid=' + that.locality_data.uuid;
                    }
                    fields += '&phone=' + encodeURIComponent(phone) + '&lat=' + lat + '&long=' + long +
                        '&scope-of-service=' + encodeURIComponent(scope) +
                        "&ancillary=" + encodeURIComponent(ancillary) + "&activities=" + encodeURIComponent(activities) + "&inpatient-service=" + encodeURIComponent(inpatient) +
                        "&staff=" + encodeURIComponent(staffs) + "&operation=" + encodeURIComponent(operation);
                }

                // ------------------------------------------------------------
                // POST
                // ------------------------------------------------------------
                {
                    // Send the data using post
                    var posting = $.post(url, fields);
                    // Put the results in a div
                    posting.done(function (data) {
                        console.log(data);
                        var data = JSON.parse(data);
                        if (data["valid"]) {
                            that.locality_uuid = data["uuid"];
                            that.getInfo();
                        } else {
                            alert(data["key"] + " can't be empty");
                        }
                    });
                }
            });
        },
        addedNewOptons: function (wrapper) {
            // SCOPE OPTIONS
            if (wrapper == "scope") {
                var html = "";
                // create nature options
                for (var i = 0; i < scope_options.length; i++) {
                    html += "<input type=\"checkbox\">" + scope_options[i] + "<br>";
                }
                html += "";
                this.$scope_of_service_input.html(html);
            }
            // ANCILLARY OPTIONS
            else if (wrapper == "ancillary") {
                var html = "";
                // create nature options
                for (var i = 0; i < scope_options.length; i++) {
                    html += "<input type=\"checkbox\">" + ancillary_options[i] + "<br>";
                }
                html += "";
                this.$ancillary_service_input.html(html);
            }
            // ACTIVITIES OPTIONS
            else if (wrapper == "activities") {
                var html = "";
                // create nature options
                for (var i = 0; i < scope_options.length; i++) {
                    html += "<input type=\"checkbox\">" + activities_options[i] + "<br>";
                }
                html += "";
                this.$activities_input.html(html);
            }

        },
        checkingOptions: function (wrapper, selected) {
            // SCOPE UPDATES
            if (wrapper == "scope") {
                var scope_inputs = this.$scope_of_service_input.find('input');
                // create nature options
                for (var i = 0; i < scope_options.length; i++) {
                    if (selected == scope_options[i]) {
                        $(scope_inputs[i]).prop('checked', true);
                    }
                }
            }
            // ANCILLARY UPDATES
            else if (wrapper == "ancillary") {
                var ancillary_service_input = this.$ancillary_service_input.find('input');
                // create nature options
                for (var i = 0; i < ancillary_options.length; i++) {
                    if (selected == ancillary_options[i]) {
                        $(ancillary_service_input[i]).prop('checked', true);
                    }
                }
            }
            // ACTIVITIES UPDATES
            else if (wrapper == "activities") {
                var activities_input = this.$activities_input.find('input');
                // create nature options
                for (var i = 0; i < activities_options.length; i++) {
                    if (selected == activities_options[i]) {
                        $(activities_input[i]).prop('checked', true);
                    }
                }
            }
        },

        showEdit: function (mode, event) {
            var isEditingMode = !(this.$editButton.is(":visible") && this.$createButton.is(":visible"));
            this.$saveButton.hide();
            this.$createButton.hide();
            this.$line_updates.show();
            if (isEditingMode && ((mode == "edit" && is_enable_edit) || (mode == "create" && isLoggedIn))) {
                if (mode == "edit" && is_enable_edit) {
                    $APP.trigger('locality.edit');
                    this.$saveButton.show();
                    this.showInfo();
                } else {
                    $APP.trigger('locality.create', {'geom': [0, 0]});
                    this.$createButton.show();
                    this.$line_updates.hide();
                    this.showDefaultEdit();
                }
                //this.showInfo();
                for (var i = 0; i < info_fields.length; i++) {
                    info_fields[i].hide();
                }
                for (var i = 0; i < edit_fields.length; i++) {
                    edit_fields[i].show();
                }
                var operation = this.$operation_input.val();
                if (operation == operation_options[operation_options.length - 1]) {
                    this.$operation_specify_input.show()
                }
            } else {
                $APP.trigger('locality.cancel');
                this.$operation_specify_input.hide();
                for (var i = 0; i < info_fields.length; i++) {
                    info_fields[i].show();
                }
                for (var i = 0; i < edit_fields.length; i++) {
                    edit_fields[i].hide();
                }
            }
        },

        setEnable: function (input) {
            this.$addButton.css({'opacity': 0.7});
            if (isLoggedIn) {
                this.$addButton.css({'opacity': 1});
            }
            is_enable_edit = input;
            if (input) {
                this.$editButton.css({'opacity': 1});
            } else {
                this.$editButton.css({'opacity': 0.7});
            }
        },

        sendEdit: function (evt, payload) {
            this.$form.attr('action', "localities/edit");
            this.$form.submit();
        },

        sendCreate: function (evt, payload) {
            this.$form.attr('action', "localities/create");
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
            this.$coordinates_long_input.val(payload.latlng.lng);
            this.$coordinates_lat_input.val(payload.latlng.lat);
        },

        showDefaultEdit: function (evt) {
            this.addedNewOptons("scope"); // this.$scope_of_service_input
            this.addedNewOptons("ancillary"); // this.$ancillary_service_input
            this.addedNewOptons("activities"); // this.$ancillary_service_input
            $(this.$nature_of_facility_input.find('option')[0]).prop('selected', true);
            $(this.$operation_input.find('option')[0]).prop('selected', true);
            this.$phone_input_int.val("");
            this.$phone_input_number.val("");
            this.$coordinates_lat_input.val(0);
            this.$coordinates_long_input.val(0);
            this.$operation_specify_input.val("");
            this.$operation_specify_input.hide();
            if (this.$cancelButton.is(":visible")) {
                this.$cancelButton.click();
            }
            this.$name_input.val("");
            this.$physical_address_input.val("");
            this.$inpatient_service_full_input.val("");
            this.$inpatient_service_part_input.val("");
            this.$staff_doctor_input.val("");
            this.$staff_nurse_input.val("");

        },
        showDefaultInfo: function (evt) {
            this.showDefaultEdit();
            this.$name.text(no_name);
            this.$nature_of_facility.text(need_information);
            this.$completenees.attr('style', 'width:0%');
            this.$completenees.text('0% Complete');
            this.$coordinates.text('lat: ' + 'n/a' + ', long: ' + 'n/a');
            this.$physical_address.text(no_physical_address);
            this.$phone.text(no_phone_found);
            this.$operation.text(no_operation_hours_found);
            this.$url.text(no_url_found);
            this.$url.removeAttr('href');
            this.$scope_of_service.html('');
            this.$scope_of_service.text(need_information);
            this.$ancillary_service.html('');
            this.$ancillary_service.text(need_information);
            this.$activities.html('');
            this.$activities.text(need_information);
            this.$staff.text(need_information);
            this.$ownership.text(need_information);
            this.$inpatient_service.text(need_information);
        },

        showInfo: function (evt) {
            // reset first
            this.showDefaultInfo();
            // set disable
            if (isLoggedIn) {
                this.setEnable(true);
            }
            console.log(this.locality_data);

            // COORDINATE AND COMPLETNESS
            {
                this.$completenees.attr('style', 'width:' + this.locality_data.completeness);
                this.$completenees.text(this.locality_data.completeness + ' Complete');
                this.$coordinates.text('lat: ' + this.locality_data.geom[1] + ', long: ' + this.locality_data.geom[0]);
                this.$coordinates_lat_input.val(this.locality_data.geom[1]);
                this.$coordinates_long_input.val(this.locality_data.geom[0]);
            }

            // LOCALITY NAME
            {
                var name = this.locality_data.values['name'];
                if (this.isHasValue(name)) {
                    this.$name.text(name);
                    this.$name_input.val(name);
                }
            }

            // NATURE OF LOCALITY
            {
                var nature = this.locality_data.values['nature_of_facility'];
                if (this.isHasValue(nature)) {
                    this.$nature_of_facility.text(nature);
                    for (var i = 0; i < nature_options.length; i++) {
                        if (nature == nature_options[i]) {
                            $(this.$nature_of_facility_input.find('option')[i]).prop('selected', true);
                            break;
                        }
                    }
                }
            }

            // PHYSICAL ADDRESS
            {
                var address = this.locality_data.values['physical_address'];
                if (this.isHasValue(address)) {
                    this.$physical_address.text(address);
                    this.$physical_address_input.val(address);
                }
            }

            // SCOPE OF SERVICE
            {
                var scope = this.locality_data.values['scope_of_service'];
                if (this.isHasValue(scope)) {
                    var scopes = scope.split("|");
                    var html = '<ul>';
                    for (i = 0; i < scopes.length; ++i) {
                        if (scopes[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += scopes[i];
                            html += '</li>';
                            this.checkingOptions("scope", scopes[i]);
                        }
                    }
                    html += '</ul>';
                    if (html != "<ul></ul>") {
                        this.$scope_of_service.html(html);
                    }
                } else {
                    //this.addedNewOption("scope", "");
                }
            }

            // ANCILLARY OF SERVICE
            {
                var ancillary = this.locality_data.values['ancillary_services'];
                if (this.isHasValue(ancillary)) {
                    var ancillary = ancillary.split("|");
                    var html = '<ul>';
                    for (i = 0; i < ancillary.length; ++i) {
                        if (ancillary[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += ancillary[i];
                            html += '</li>';
                            this.checkingOptions("ancillary", ancillary[i]);
                        }
                    }
                    html += '</ul>';
                    if (html != "<ul></ul>") {
                        this.$ancillary_service.html(html);
                    }
                } else {
                    //this.addedNewOption("ancillary", "");
                }
            }

            // ACTIVITIES OF SERVICE
            {
                var activities = this.locality_data.values['activities'];
                if (this.isHasValue(activities)) {
                    var activities = activities.split("|");
                    var html = '<ul>';
                    for (i = 0; i < activities.length; ++i) {
                        if (activities[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += activities[i];
                            html += '</li>';
                            this.checkingOptions("activities", activities[i]);
                        }
                    }
                    html += '</ul>';
                    if (html != "<ul></ul>") {
                        this.$activities.html(html);
                    }
                } else {
                    //this.addedNewOption("activities", "");
                }
            }

            // INPATIENT-SERVICE
            {
                var inpatient = this.locality_data.values['inpatient_service'];
                if (this.isHasValue(inpatient)) {
                    var inpatient = inpatient.split("|");
                    if (inpatient.length >= 1 && inpatient[0] != "") {
                        // reinit view
                        this.$inpatient_service.html("<span id=\"locality-inpatient-service-full\">-</span> full time beds, <span id=\"locality-inpatient-service-part\">-</span> part time beds");
                        this.$inpatient_service_full = $('#locality-inpatient-service-full');
                        this.$inpatient_service_part = $('#locality-inpatient-service-part');
                        // fill value
                        this.$inpatient_service_full.text(parseInt(inpatient[0], 10));
                        this.$inpatient_service_full_input.val(parseInt(inpatient[0], 10));
                    }
                    if (inpatient.length >= 2 && inpatient[1] != "") {
                        this.$inpatient_service_part.text(parseInt(inpatient[1], 10));
                        this.$inpatient_service_part_input.val(parseInt(inpatient[1], 10));
                    }
                }
            }

            // STAFFS
            {
                var staff = this.locality_data.values['staff'];
                if (this.isHasValue(staff)) {
                    var staff = staff.split("|");
                    if (staff.length >= 1 && staff[0] != "") {
                        // reinit view
                        this.$staff.html("<span id=\"locality-staff-doctor\">-</span> full time equivalent doctors and <span id=\"locality-staff-nurse\">-</span> full time equivalent nurses");
                        this.$staff_doctor = $('#locality-staff-doctor');
                        this.$staff_nurse = $('#locality-staff-nurse');
                        // fill value
                        this.$staff_doctor.text(parseInt(staff[0], 10));
                        this.$staff_doctor_input.val(parseInt(staff[0], 10));
                    }
                    if (staff.length >= 2 && staff[1] != "") {
                        this.$staff_nurse.text(parseInt(staff[1], 10));
                        this.$staff_nurse_input.val(parseInt(staff[1], 10));
                    }
                }
            }

            // OWNERSHIP
            {
                var ownership = this.locality_data.values['ownership'];
                if (this.isHasValue(ownership)) {
                    this.$ownership.text(ownership);
                    for (var i = 0; i < ownership_options.length; i++) {
                        if (ownership == ownership_options[i]) {
                            $(this.$ownership_input.find('option')[i]).prop('selected', true);
                            break;
                        }
                    }
                }
            }

            // OPERATION
            {
                var operation = this.locality_data.values['operation'];
                if (this.isHasValue(operation)) {
                    this.$operation.text(operation);
                    for (var i = 0; i < operation_options.length; i++) {
                        if (operation == operation_options[i]) {
                            $(this.$operation_input.find('option')[i]).prop('selected', true);
                            break;
                        } else {
                            if (i == operation_options.length - 1) {
                                $(this.$operation_input.find('option')[operation_options.length - 1]).prop('selected', true);
                                this.$operation_specify_input.val(operation);
                            }
                        }
                    }
                }
            }

            // PHONE
            {
                var phone = this.locality_data.values['phone'];
                if (this.isHasValue(phone)) {
                    this.$phone.text(phone);
                    phone = phone.replace("+", "");
                    var phones = phone.split("-");
                    this.$phone_input_int.val(phones[0]);
                    this.$phone_input_number.val(phones[1]);
                }
            }

            if (this.locality_data.values['url']) {
                this.$url.text(this.locality_data.values['url']);
                if (!this.locality_data.values['url'].startsWith('http://')) {
                    this.locality_data.values['url'] = 'http://' + this.locality_data.values['url'];
                }
                this.$url.attr('href', this.locality_data.values['url']);
            }
        },
        isHasValue: function (value) {
            if (value && value.length > 0) {
                return true;
            } else {
                return false;
            }
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
            $APP.on('sidebar.option-onchange', function (evt, payload) {
                self.onchange(payload.element);
            });
        },
        onchange: function (element) {
            if (element.id == this.$operation_input.attr('id')) {
                if (element.value == operation_options[operation_options.length - 1]) {
                    this.$operation_specify_input.show();
                } else {
                    this.$operation_specify_input.hide();
                }
            } else if (element.id == this.$coordinates_lat_input.attr('id')) {
                $APP.trigger('locality.coordinate-changed', {'geom': [this.$coordinates_long_input.val(), this.$coordinates_lat_input.val()]});
            } else if (element.id == this.$coordinates_long_input.attr('id')) {
                $APP.trigger('locality.coordinate-changed', {'geom': [this.$coordinates_long_input.val(), this.$coordinates_lat_input.val()]});
            }
        }
    }

// return module
    return module;
}());
