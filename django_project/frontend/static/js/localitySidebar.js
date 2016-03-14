window.LocalitySidebar = (function () {
    "use strict";
    var separator = "|";
    var special_attribute = ["uuid", "geom", "long", "lat", "nature_of_facility", "inpatient_service", "staff", "ownership", "nature_of_facility",
        "scope_of_service", "notes", "ancillary_services", "operation", "activities", "data_source",
        "name", "email", "mobile", "phone", "physical_address", "services", "tags", "defining_hours"];

    var nature_options = ["", "clinic without beds", "clinic with beds", "first referral hospital", "second referral hospital or General hospital", "tertiary level including University hospital"];
    var scope_options = ["specialized care", "general acute care", "rehabilitation care", "old age/hospice care"];
    var ancillary_options = ["Operating theater", "laboratory", "imaging equipment", "intensive care unit", "Emergency department"];
    var activities_options = ["medicine and medical specialties", "surgery and surgical specialties", "Maternal and women health", "pediatric care", "mental health", "geriatric care", "social care"];
    var ownership_options = ["", "public", "private not for profit", "private commercial"];
    var notes_options = ["Outpatient consultation", "In-patient hospitalization"];
    var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    var time_default = ["09:00", "17:00"];
    var need_information = "needs information";
    var no_physical_address = "..please update address";
    var no_phone_found = "..please update number";
    var no_operation_hours_found = "..please define operating hours";
    var no_scope_found = "..please define scope of service";
    var no_anchillary_found = "..please define ancillary services";
    var no_activities_found = "..please define ancillary activities";
    var no_inpatient_found = "..please define number of full time/part time beds";
    var no_notes_found = "..please define notes hospitalisation and outpatient consultation";
    var no_staff_found = "..please define full time doctors and full time nurses";
    var no_ownership_found = "..please define ownership status";
    var no_tag_found = "please add comma separated tags";
    var no_others_found = "please use this field to define any additional services available from this location";
    var no_name = "No Name";
    var is_enable_edit = false;
    var info_fields = [];
    var edit_fields = [];
    var others_attr = [];
    // private variables and functions

    // constructor
    var module = function () {
        this.$sidebar = $('#locality-info');
        // new style
        this.$line_updates = $('#line-updates');
        this.$name = $('#locality-name');
        this.$nature_of_facility = $('#locality-nature-of-facility');
        this.$completenees = $('#locality-completeness');
        this.$coordinates = $('#locality-coordinates');
        this.$physical_address = $('#locality-physical-address');
        this.$phone = $('#locality-phone');
        this.$scope_of_service = $('#locality-scope-of-service');
        this.$ancillary_service = $('#locality-ancillary-service');
        this.$activities = $('#locality-activities');
        this.$ownership = $('#locality-ownership');
        this.$inpatient_service = $('#locality-inpatient-service');
        this.$staff = $('#locality-staff');
        this.$notes = $('#locality-notes');
        this.$notes_text = $('#locality-notes-text');
        this.$tag_data = $('#tag-data');
        this.$defining_hours_section = $('#locality-operating-hours-section');
        this.$defining_hours = $('#locality-operating-hours');

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
        this.$notes_input = $('#locality-notes-input');

        this.$other_add = $('#others-add');
        this.$other_data = $('#others-data');
        this.$other_data_input = $('#others-data-input');

        this.$tag_input = $('#tag-input');
        this.$tag_input_text = $('#tag-input-text');
        this.$tag_input_text_box = $('#tag-input-text-box');
        this.$tag_input_error_warning = $('#tag-input-error-warning');
        this.$uploader = $('#uploader');
        this.$lastupdate = $('#last_update');

        this.$defining_hours_input = $('#locality-operating-hours-input');
        this.$defining_hours_input_table = $('#locality-operating-hours-input-table');
        this.$defining_hours_input_result = $('#locality-operating-hours-input-result');

        // create nature options
        for (var i = 0; i < nature_options.length; i++) {
            this.$nature_of_facility_input.append("<option value=\"" + nature_options[i] + "\">" + nature_options[i] + "</option>");
        }
        // create ownershipe options
        for (var i = 0; i < ownership_options.length; i++) {
            this.$ownership_input.append("<option value=\"" + ownership_options[i] + "\">" + ownership_options[i] + "</option>");
        }
        // set info field array
        info_fields.push(this.$editButton);
        info_fields.push(this.$addButton);
        info_fields.push(this.$name);
        info_fields.push(this.$physical_address);
        info_fields.push(this.$phone);
        info_fields.push(this.$nature_of_facility);
        info_fields.push(this.$scope_of_service);
        info_fields.push(this.$ownership);
        info_fields.push(this.$ancillary_service);
        info_fields.push(this.$activities);
        info_fields.push(this.$inpatient_service);
        info_fields.push(this.$staff);
        info_fields.push(this.$coordinates);
        info_fields.push(this.$notes);
        info_fields.push(this.$other_data);
        info_fields.push(this.$tag_data);
        info_fields.push(this.$defining_hours_section);

        // set editfield array
        edit_fields.push(this.$cancelButton);
        edit_fields.push(this.$name_input);
        edit_fields.push(this.$physical_address_input);
        edit_fields.push(this.$phone_input);
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
        edit_fields.push(this.$notes_input);
        edit_fields.push(this.$other_add);
        edit_fields.push(this.$other_data_input);
        edit_fields.push(this.$tag_input);
        edit_fields.push(this.$tag_input_text);
        edit_fields.push(this.$defining_hours_input);

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
                var isFormValid = true;
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

                    // GET SCOPE CHILD
                    var scope_inputs = that.$scope_of_service_input.find('input');
                    var scope = "";
                    for (var i = 0; i < scope_inputs.length; i++) {
                        if ($(scope_inputs[i]).prop('checked')) {
                            scope += scope_options[i] + separator;
                        }
                    }
                    if (scope == separator) {
                        scope = "";
                    }

                    // GET ANCILLARY CHILD
                    var ancillary_inputs = that.$ancillary_service_input.find('input');
                    var ancillary = "";
                    for (var i = 0; i < ancillary_inputs.length; i++) {
                        if ($(ancillary_inputs[i]).prop('checked')) {
                            ancillary += ancillary_options[i] + separator;
                        }
                    }
                    if (ancillary == separator) {
                        ancillary = "";
                    }

                    // GET ACTIVITIES CHILD
                    var activities_input = that.$activities_input.find('input');
                    var activities = "";
                    for (var i = 0; i < activities_input.length; i++) {
                        if ($(activities_input[i]).prop('checked')) {
                            activities += activities_options[i] + separator;
                        }
                    }
                    if (activities == separator) {
                        activities = "";
                    }

                    // GET NOTES CHILD
                    var notes_input = that.$notes_input.find('input');
                    var notes = "";
                    for (var i = 0; i < notes_input.length; i++) {
                        if ($(notes_input[i]).prop('checked')) {
                            notes += notes_options[i] + separator;
                        }
                    }
                    if (notes == separator) {
                        notes = "";
                    }

                    // GET INPATIENT_SERVICE CHILD
                    var inpatient_service = that.$inpatient_service_full_input.val() + separator + that.$inpatient_service_part_input.val();
                    if (inpatient_service == separator) {
                        inpatient_service = "";
                    }

                    // GET STAFFS CHILD
                    var staffs = that.$staff_doctor_input.val() + separator + that.$staff_nurse_input.val();
                    if (staffs == separator) {
                        staffs = "";
                    }

                    // GET PHONE
                    var phone = "";
                    if (that.$phone_input_int.val().length > 0 || that.$phone_input_number.val().length > 0) {
                        phone = "+" + that.$phone_input_int.val() + "-" + that.$phone_input_number.val();
                    }

                    // GET TAG
                    var tags = that.$tag_input_text_box.val();
                    tags = tags.split(",");
                    tags = tags.getUnique();
                    for (var i = 0; i < tags.length; i++) {
                        tags[i] = $.trim(tags[i]);
                        if (tags[i].length > 0 && tags[i].length < 3) {
                            isFormValid = false;
                        }
                    }
                    tags = tags.join(separator);
                    tags = "|" + tags + "|";

                    if (that.locality_data != null) {
                        fields += '&uuid=' + that.locality_data.uuid;
                    }
                    fields += '&phone=' + encodeURIComponent(phone) + '&lat=' + lat + '&long=' + long +
                        '&scope_of_service=' + encodeURIComponent(scope) +
                        "&ancillary_services=" + encodeURIComponent(ancillary) + "&activities=" + encodeURIComponent(activities) + "&inpatient_service=" + encodeURIComponent(inpatient_service) +
                        "&staff=" + encodeURIComponent(staffs) + "&notes=" + encodeURIComponent(notes) + "&tags=" + encodeURIComponent(tags);

                    // GET DEFINING HOURS
                    fields += "&defining_hours=" + that.getDefiningHoursFormat()["format1"];
                    // GET OTHERS
                    var others = that.$other_data_input.find("div");
                    for (var i = 0; i < others.length; i++) {
                        var attr = $(others[i]).find(".attribute").val();
                        var newattr = attr.replace(" ", "_").toLowerCase();
                        var value = $(others[i]).find(".value").val();

                        var isValid = true;
                        for (var j = 0; j < special_attribute.length; j++) {
                            if (newattr == special_attribute[j]) {
                                isValid = false;
                                break;
                            }
                        }

                        if (!isValid) {
                            alert("cannot create " + attr + " as new attribute");
                            isFormValid = false;
                            break;
                        }

                        if (newattr != "" && value != "") {
                            fields += "&" + newattr + "=" + encodeURIComponent(value);
                            delete others_attr[that.getIndex(others_attr, newattr)];
                        }
                    }

                    // check the attribute that should be deleted
                    for (var i = 0; i < others_attr.length; i++) {
                        if (typeof others_attr[i] !== 'undefined') {
                            fields += "&" + others_attr[i] + "=" + encodeURIComponent("");
                        }
                    }
                }

                // ------------------------------------------------------------
                // POST
                // ------------------------------------------------------------
                {
                    if (isFormValid) {
                        //Send the data using post
                        var posting = $.post(url, fields);
                        // Put the results in a div
                        posting.done(function (data) {
                            var data = JSON.parse(data);
                            if (data["valid"]) {
                                that.locality_uuid = data["uuid"];
                                $APP.trigger('set.hash.silent', {'locality': that.locality_uuid});
                                that.getInfo();
                            } else {
                                alert(data["key"] + " can't be empty");
                            }
                        });
                    }
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
            // notes OPTIONS
            else if (wrapper == "notes") {
                var html = "";
                // create nature options
                for (var i = 0; i < notes_options.length; i++) {
                    html += "<input type=\"checkbox\">" + notes_options[i] + "<br>";
                }
                html += "";
                this.$notes_input.html(html);
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
            // notes UPDATES
            else if (wrapper == "notes") {
                var notes_input = this.$notes_input.find('input');
                // create nature options
                for (var i = 0; i < notes_options.length; i++) {
                    if (selected == notes_input[i]) {
                        $(notes_input[i]).prop('checked', true);
                    }
                }
            }
        },

        showEdit: function (mode, event) {
            var isEditingMode = !(this.$editButton.is(":visible") && this.$createButton.is(":visible"));
            this.$saveButton.hide();
            this.$createButton.hide();
            this.$line_updates.show();
            if (isEditingMode && !isLoggedIn) {
                setCookie("type", "add", 30);
                setCookie("center", APP.getCenterOfMap().lat + "," + APP.getCenterOfMap().lng, 30);
                setCookie("zoom", APP.getZoomOfMap(), 30);
                window.location.href = "/signin/";
            } else if (isEditingMode && ((mode == "edit" && is_enable_edit) || (mode == "create"))) {
                if (mode == "edit" && is_enable_edit) {
                    this.$saveButton.show();
                    this.showInfo();
                    $APP.trigger('locality.edit');
                }
                else {
                    this.$createButton.show();
                    this.$line_updates.hide();
                    this.showDefaultEdit();
                    $APP.trigger('locality.create');
                }
                //this.showInfo();
                for (var i = 0; i < info_fields.length; i++) {
                    info_fields[i].hide();
                }
                for (var i = 0; i < edit_fields.length; i++) {
                    edit_fields[i].show();
                }
            } else {
                $APP.trigger('locality.cancel');
                for (var i = 0; i < info_fields.length; i++) {
                    info_fields[i].show();
                }
                for (var i = 0; i < edit_fields.length; i++) {
                    edit_fields[i].hide();
                }
            }
        },

        setEnable: function (input) {
            this.$addButton.css({'opacity': 1});
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

        getDefiningHoursFormat: function () {
            var format1 = ""; // for send to database
            var format2 = ""; // for show in UI
            var list_hours = [];
            for (var i = 0; i < days.length; i++) {
                var list_input = $('#' + days[i]).find('input');
                var checked = $(list_input[0]).prop('checked');
                var split = $('#' + days[i]).find('.unsplit').css('opacity') == 1 ? true : false;
                var time1 = [$(list_input[1]).val(), $(list_input[2]).val()];
                var time2 = [$(list_input[3]).val(), $(list_input[4]).val()];

                //format1
                if (checked) {
                    //format 1
                    format1 += time1.join("-");
                    format1 += "-";
                    if (split) {
                        format1 += time2.join("-");
                    } else {
                        format1 += "-";
                    }
                } else {
                    //format 1
                    format1 += "-";
                }
                format1 += "|"

                time1 = ["<b>" + $(list_input[1]).val() + "</b>", "<b>" + $(list_input[2]).val() + "</b>"];
                time2 = ["<b>" + $(list_input[3]).val() + "</b>", "<b>" + $(list_input[4]).val() + "</b>"];
                //format2
                var isSame = false;
                if (i != 0) {
                    var isChecked = checked == list_hours[i - 1][1];
                    var isSplit = split == list_hours[i - 1][2];
                    var isTime1Same = time1[0] == list_hours[i - 1][3][0] && time1[1] == list_hours[i - 1][3][1];
                    var isTime2Same = time2[0] == list_hours[i - 1][4][0] && time2[1] == list_hours[i - 1][4][1];
                    if (isChecked && isSplit && isTime1Same && isTime2Same) {
                        isSame = true;
                    }
                }
                list_hours.push([days[i], checked, split, time1, time2, isSame]);
            }
            list_hours.push([days]);
            // lets render the text
            var last_init_hour = 0;
            for (var i = 0; i < list_hours.length; i++) {
                if (i != 0) {
                    if (list_hours[i][5] != true || i == list_hours.length - 1) {
                        // render
                        if (last_init_hour != i - 1) {
                            // render to
                            if (list_hours[i - 1][1] == true) {
                                format2 += list_hours[last_init_hour][0] + " to " + list_hours[i - 1][0] + " : " + list_hours[last_init_hour][3].join("-");
                                if (list_hours[last_init_hour][2] == true) {
                                    format2 += " and " + list_hours[last_init_hour][4].join("-");
                                }
                                format2 += "<br>";
                            }
                        } else {
                            if (list_hours[i - 1][1] == true) {
                                format2 += list_hours[last_init_hour][0] + " : " + list_hours[last_init_hour][3].join("-");
                                if (list_hours[last_init_hour][2] == true) {
                                    format2 += " and " + list_hours[last_init_hour][4].join("-");
                                }
                                format2 += "<br>";
                            }
                        }
                        last_init_hour = i;
                    }
                }
            }
            //check for 24 hours
            format2 = format2.replaceAll("<b>00:00</b>-<b>23:59</b>", "<b>24H</b>");
            format2 = format2.replaceAll("<b>00:00</b>-<b>00:00</b>", "<b>24H</b>");
            //check for 24/7 hours
            format2 = format2.replaceAll("Monday to Sunday : <b>24H</b><br>", "<b>24/7</b>");
            return {"format1": format1, "format2": format2};
        },
        setDefiningHour: function (days_index, from1, to1, from2, to2) {
            var list_input = $('#' + days[days_index]).find('input');
            if (typeof from1 !== 'undefined' && from1 != "") {
                $(list_input[0]).prop('checked', true);
            } else {
                $(list_input[0]).prop('checked', false);
            }
            if (typeof from1 !== 'undefined' && from1 != "") $(list_input[1]).val(from1);
            if (typeof to1 !== 'undefined' && to1 != "") $(list_input[2]).val(to1);
            if (typeof from2 !== 'undefined' && from2 != "") {
                $('#' + days[days_index]).find('.split').click();
                $(list_input[3]).val(from2);
            }
            if (typeof to2 !== 'undefined' && to2 != "") $(list_input[4]).val(to2);
        },
        showDefaultEdit: function (evt) {
            $('#full-list').html("");
            $('#see-more-list').show();
            $("#locality-statistic").hide();
            $("#locality-info").show();
            $("#locality-default").hide();
            this.addedNewOptons("scope"); // this.$scope_of_service_input
            this.addedNewOptons("ancillary"); // this.$ancillary_service_input
            this.addedNewOptons("activities"); // this.$ancillary_service_input
            this.addedNewOptons("notes"); // this.$notes_input
            $(this.$nature_of_facility_input.find('option')[0]).prop('selected', true);
            this.$phone_input_int.val("");
            this.$phone_input_number.val("");
            this.$coordinates_lat_input.val(0);
            this.$coordinates_long_input.val(0);
            if (this.$cancelButton.is(":visible")) {
                this.$cancelButton.click();
            }
            this.$name_input.val("");
            this.$physical_address_input.val("");
            this.$inpatient_service_full_input.val("");
            this.$inpatient_service_part_input.val("");
            this.$staff_doctor_input.val("");
            this.$staff_nurse_input.val("");
            this.$tag_input.html("");
            this.$tag_input_text_box.val("");
            this.$other_data_input.html("");

            // defining hours setup
            this.$defining_hours_input_table.html("");
            for (var i = 0; i < days.length; i++) {
                var checked = "";
                var html = '<tr id="' + days[i] + '"><td>';
                html += '<input class="daycheckbox" type="checkbox" ' + checked + '>' + days[i] + '</td>';
                html += '<td class="time1" style="cursor: default"> from <input class="timepicker" type="text" value="' + time_default[0] + '"/> to <input class="timepicker" type="text" value="' + time_default[1] + '"/>';
                html += '<td class="split" onclick="split(this)" style="cursor: pointer"><a>split</a>';
                html += '</td>';
                html += '<td class="time2" style="opacity: 0.0; cursor: default"> from <input class="timepicker" type="text" value="00:00" disabled /> to <input class="timepicker" type="text" value="00:00" disabled/>';
                html += '<td class="unsplit" onclick="unsplit(this)" style="opacity: 0.0; cursor: default"><a>unsplit</a>';
                html += '</td></tr>';
                this.$defining_hours_input_table.append(html);
            }
            this.$defining_hours_input_result.html(this.getDefiningHoursFormat()["format2"]);

            var that = this;
            $("input.daycheckbox").change(function () {
                that.$defining_hours_input_result.html(that.getDefiningHoursFormat()["format2"]);
            });
            $('input.timepicker').timepicker({
                timeFormat: 'HH:mm',
                interval: 15, // 15 minutes});
                change: function (time) {
                    that.$defining_hours_input_result.html(that.getDefiningHoursFormat()["format2"]);
                },
            })

        },
        showDefaultInfo: function (evt) {
            $APP.trigger('locality.history-hide');
            this.showDefaultEdit();
            this.$name.text(no_name);
            this.$nature_of_facility.text(need_information);
            this.$completenees.attr('style', 'width:0%');
            this.$completenees.text('0% Complete');
            this.$coordinates.text('lat: ' + 'n/a' + ', long: ' + 'n/a');
            this.$physical_address.text(no_physical_address);
            this.$phone.text(no_phone_found);
            this.$scope_of_service.html('');
            this.$scope_of_service.text(no_scope_found);
            this.$ancillary_service.html('');
            this.$ancillary_service.text(no_anchillary_found);
            this.$activities.html('');
            this.$activities.text(no_activities_found);
            this.$staff.text(no_staff_found);
            this.$ownership.text(no_ownership_found);
            this.$inpatient_service.text(no_inpatient_found);
            this.$notes_text.text(no_notes_found);

            this.$other_data.html(no_others_found);
            this.$other_data_input.html("");
            this.$tag_data.html(no_tag_found);
            others_attr = [];
            this.$lastupdate.text("11 may 2015 17:23:15");
            this.$uploader.text("@sharehealthdata");
            this.$uploader.attr("href", "profile/sharehealthdata");
            this.$defining_hours.html(no_operation_hours_found);
        },

        showInfo: function (evt) {
            // reset first
            this.showDefaultInfo();
            // COORDINATE AND COMPLETNESS
            {
                this.$completenees.attr('style', 'width:' + this.locality_data.completeness);
                this.$completenees.text(this.locality_data.completeness + ' Complete');
                this.$coordinates.text('lat: ' + this.locality_data.geom[1] + ', long: ' + this.locality_data.geom[0]);
                this.$coordinates_lat_input.val(this.locality_data.geom[1]);
                this.$coordinates_long_input.val(this.locality_data.geom[0]);
            }

            if (this.locality_data.updates) {
                var updates = this.locality_data.updates;
                if (updates[0]) {
                    this.$lastupdate.text(getDateString(updates[0]['last_update']));
                    this.$lastupdate.data("data", {date: updates[0]['last_update']});
                    this.$uploader.text("@" + updates[0]['nickname']);
                    this.$uploader.attr("href", "profile/" + updates[0]['uploader']);
                }
            }

            var keys = [];
            for (var k in this.locality_data.values) keys.push(k);

            // LOCALITY NAME
            {
                var name = this.locality_data.values['name'];
                delete keys[this.getIndex(keys, 'name')];
                if (this.isHasValue(name)) {
                    this.$name.text(name);
                    this.$name_input.val(name);
                }
            }

            // NATURE OF LOCALITY
            {
                var nature = this.locality_data.values['nature_of_facility'];
                delete keys[this.getIndex(keys, 'nature_of_facility')];
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
                delete keys[this.getIndex(keys, 'physical_address')];
                if (this.isHasValue(address)) {
                    this.$physical_address.text(address);
                    this.$physical_address_input.val(address);
                }
            }
            // SCOPE OF SERVICE
            {
                var scope = this.locality_data.values['scope_of_service'];
                delete keys[this.getIndex(keys, 'scope_of_service')];
                if (this.isHasValue(scope)) {
                    var scopes = scope.split(separator);
                    var html = '<ul>';
                    for (i = 0; i < scopes.length; ++i) {
                        if (scopes[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += '<a href="/map?attribute=' + scopes[i] + '&uuid=' + this.locality_uuid + '"  >' + scopes[i] + '</a>';
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
                delete keys[this.getIndex(keys, 'ancillary_services')];
                if (this.isHasValue(ancillary)) {
                    var ancillary = ancillary.split(separator);
                    var html = '<ul>';
                    for (i = 0; i < ancillary.length; ++i) {
                        if (ancillary[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += '<a href="/map?attribute=' + ancillary[i] + '&uuid=' + this.locality_uuid + '" >' + ancillary[i] + '</a>';
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
                delete keys[this.getIndex(keys, 'activities')];
                if (this.isHasValue(activities)) {
                    var activities = activities.split(separator);
                    var html = '<ul>';
                    for (i = 0; i < activities.length; ++i) {
                        if (activities[i].length > 0) {
                            html += '<li><i class="fa fa-caret-right"></i>';
                            html += '<a href="/map?attribute=' + activities[i] + '&uuid=' + this.locality_uuid + '" >' + activities[i] + '</a>';
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

            // NOTES
            {
                var notes = this.locality_data.values['notes'];
                delete keys[this.getIndex(keys, 'notes')];
                if (this.isHasValue(notes)) {
                    var notes_input = this.$notes_input.find('input');
                    for (var i = 0; i < notes_options.length; i++) {
                        if (notes.indexOf(notes_options[i]) !== -1) {
                            $(notes_input[i]).prop('checked', true);
                        }
                    }
                    var notes = notes.split(separator);
                    notes.pop();
                    this.$notes_text.html(notes.join(" and "));
                }
            }

            // INPATIENT_SERVICE
            {
                var inpatient_service = this.locality_data.values['inpatient_service'];
                delete keys[this.getIndex(keys, 'inpatient_service')];
                if (this.isHasValue(inpatient_service)) {
                    var inpatient_service = inpatient_service.split(separator);
                    if (inpatient_service.length >= 1 && (inpatient_service[0] != "" | inpatient_service[1] != "")) {
                        // reinit view
                        this.$inpatient_service.html("<span id=\"locality-inpatient-service-full\">-</span> full time beds, <span id=\"locality-inpatient-service-part\">-</span> part time beds");
                        this.$inpatient_service_full = $('#locality-inpatient-service-full');
                        this.$inpatient_service_part = $('#locality-inpatient-service-part');
                    }
                    if (inpatient_service.length >= 1 && inpatient_service[0] != "") {
                        // fill value
                        this.$inpatient_service_full.text(parseInt(inpatient_service[0], 10));
                        this.$inpatient_service_full_input.val(parseInt(inpatient_service[0], 10));
                    }
                    if (inpatient_service.length >= 2 && inpatient_service[1] != "") {
                        this.$inpatient_service_part.text(parseInt(inpatient_service[1], 10));
                        this.$inpatient_service_part_input.val(parseInt(inpatient_service[1], 10));
                    }
                }
            }

            // STAFFS
            {
                var staff = this.locality_data.values['staff'];
                delete keys[this.getIndex(keys, 'staff')];
                if (this.isHasValue(staff)) {
                    var staff = staff.split(separator);
                    if (staff.length >= 1 && (staff[0] != "" | staff[1] != "")) {
                        // reinit view
                        this.$staff.html("<span id=\"locality-staff-doctor\">-</span> full time doctors, <span id=\"locality-staff-nurse\">-</span> full time nurses");
                        this.$staff_doctor = $('#locality-staff-doctor');
                        this.$staff_nurse = $('#locality-staff-nurse');
                    }
                    if (staff[0] != "") {
                        // fill value
                        this.$staff_doctor.text(parseInt(staff[0], 10));
                        this.$staff_doctor_input.val(parseInt(staff[0], 10));
                    }
                    if (staff[1] != "") {
                        this.$staff_nurse.text(parseInt(staff[1], 10));
                        this.$staff_nurse_input.val(parseInt(staff[1], 10));
                    }
                }
            }

            // OWNERSHIP
            {
                var ownership = this.locality_data.values['ownership'];
                delete keys[this.getIndex(keys, 'ownership')];
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
            // PHONE
            {
                var phone = this.locality_data.values['phone'];
                delete keys[this.getIndex(keys, 'phone')];
                if (this.isHasValue(phone)) {
                    this.$phone.text(phone);
                    phone = phone.replace("+", "");
                    var phones = phone.split("-");
                    this.$phone_input_int.val(phones[0]);
                    this.$phone_input_number.val(phones[1]);
                }
            }

            // DEFINING HOURS
            {
                var hours = this.locality_data.values['defining_hours'];
                delete keys[this.getIndex(keys, 'defining_hours')];
                if (this.isHasValue(hours)) {
                    var hours_each_day = hours.split(separator);
                    for (var i = 0; i < hours_each_day.length; i++) {
                        var hours = hours_each_day[i].split("-");
                        this.setDefiningHour(i, hours[0], hours[1], hours[2], hours[3]);
                    }
                    this.$defining_hours_input_result.html(this.getDefiningHoursFormat()["format2"]);
                    this.$defining_hours.html(this.getDefiningHoursFormat()["format2"]);
                }
            }


            // TAGS
            {
                var tags = this.locality_data.values['tags'];
                delete keys[this.getIndex(keys, 'tags')];
                if (this.isHasValue(tags)) {
                    var tags = tags.split(separator);
                    tags = cleanArray(tags);
                    this.$tag_input_text_box.val(tags.join(","));
                    for (var i = 0; i < tags.length; i++) {
                        if (tags[i] != "") {
                            // render
                            if (this.$tag_data.html() == no_tag_found) {
                                this.$tag_data.html("");
                            }
                            this.$tag_data.append("<li><i class=\"fa fa-caret-right\"></i> <a href=\"map?tag=" + tags[i] + "\">" + tags[i] + "</a></li>");
                        }
                    }
                }
            }
            // OTHER
            {
                keys = cleanArray(keys);
                if (keys.length > 0) {
                    this.$other_data.html("");
                }
                for (var i = 0; i < keys.length; i++) {
                    if (typeof keys[i] !== 'undefined') {
                        this.addOther(keys[i].replace("_", " "), this.locality_data.values[keys[i]]);
                        others_attr.push(keys[i]);
                    }
                }
            }
        },
        isHasValue: function (value) {
            if (value && value.length > 0) {
                return true;
            } else {
                return false;
            }
        },
        getIndex: function (array, value) {
            var index = -99;
            for (var i = 0; i < array.length; i++) {
                if (array[i] == value) {
                    index = i;
                    break;
                }
            }
            return index;
        },

        getInfo: function (evt, payload) {
            var self = this;
            var url = '/localities/' + this.locality_uuid;
            if (payload) {
                if (payload.changeset) {
                    url += "/" + payload.changeset;
                }
            }
            $.getJSON(url, function (data) {
                self.locality_data = data;
                self.$sidebar.trigger('show-info');
                if (payload) {
                    var zoomto = payload.zoomto;
                } else {
                    var zoomto = false;
                }
                $APP.trigger('locality.info', {
                    'locality_uuid': self.locality_uuid,
                    'locality_name': data.values.name,
                    'geom': data.geom,
                    'zoomto': zoomto
                });
                var updates = data.updates;
                if (updates.length <= 1) {
                    $("#see-more-list").hide();
                }
                $("#see-more-list").data("data", {uuid: self.locality_uuid});
                if (data.history) {
                    self.setEnable(false);
                    $APP.trigger('locality.history-show', {
                        'geom': data.geom
                    });
                } else {
                    self.setEnable(true);
                    $APP.trigger('locality.history-hide', {
                        'geom': data.geom
                    });
                }
            });
        },

        _bindExternalEvents: function () {
            var self = this;

            $APP.on('locality.map.click', function (evt, payload) {
                self.locality_uuid = payload.locality_uuid;
                self.$sidebar.trigger('get-info', {'zoomto': payload.zoomto, 'changeset': payload.changeset});
            });
            $APP.on('locality.map.move', function (evt, payload) {
                self.$sidebar.trigger('update-coordinates', payload);
            });
            $APP.on('sidebar.option-onchange', function (evt, payload) {
                self.onchange(payload.element);
            });
            $APP.on('sidebar.option-add', function (evt, payload) {
                self.addOption(payload.element, "");
            });
            $APP.on('sidebar.other-add', function (evt, payload) {
                self.addOther("", "");
            });
            $APP.on('sidebar.tag-onchange', function (evt, payload) {
                self.checkTag(payload.value);
            });
            $APP.on('sidebar.split-event', function (evt, payload) {
                self.$defining_hours_input_result.html(self.getDefiningHoursFormat()["format2"]);
            });
        },
        onchange: function (element) {
            if (element.id == this.$coordinates_lat_input.attr('id')) {
                $APP.trigger('locality.coordinate-changed', {'geom': [this.$coordinates_long_input.val(), this.$coordinates_lat_input.val()]});
            } else if (element.id == this.$coordinates_long_input.attr('id')) {
                $APP.trigger('locality.coordinate-changed', {'geom': [this.$coordinates_long_input.val(), this.$coordinates_lat_input.val()]});
            }
        },
        addOption: function (element, value) {
            //if (element.id == this.$url_input_add.attr('id')) {
            //    this.addOptionUrl(value);
            //}
        },
        addOther: function (attribute, value) {
            var html = "<div class=\"input\">";
            html += "<input type=\"text\" placeholder=\"Attribute\" class=\"attribute\" value=\"" + attribute + "\" />";
            html += "<input type=\"text\" placeholder=\"Value\"  class=\"value\" value=\"" + value + "\" />";
            html += "<span class=\"remove_option\">  -  </span>"
            html += "</div>";
            this.$other_data_input.append(html);

            if (attribute != "" && value != "") {
                var html = "<p><strong>" + attribute + ": </strong>";
                html += "<span>" + value + "</span></p>";
                this.$other_data.append(html);
            }
        },
        checkTag: function (value) {
            var tags = value.split(",");
            var isValid = true;
            if (value.length != 0) {
                for (var i = 0; i < tags.length; i++) {
                    if (tags[i].length > 0 && tags[i].length < 3) {
                        isValid = false;
                    }
                }
            }

            if (isValid) {
                this.$tag_input_error_warning.hide();
            } else {
                this.$tag_input_error_warning.show();
            }
        }
    }

    return module;
}());
