define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        attributes_and_element: {
            'locality-name': {default: "No Name", attribute: 'name'},
            'last_update': {default: "-", attribute: 'changeset_timestamp'},
            'uploader': {default: "-", attribute: 'changeset_user'},
            'locality-amenity': {default: "needs information", attribute: 'amenity'},
            'locality-nature-of-facility': {default: "needs information", attribute: 'nature_of_facility'},
            'locality-completeness': {default: "0% Complete", attribute: 'completeness'},
            'locality-coordinates': {default: "lat: n/a, long: n/a", attribute: 'coordinates'},
            'locality-physical-address': {default: "..please update address", attribute: "physical_address"},
            'locality-phone': {default: "..please update phone number", attribute: "phone"},
            'locality-url': {default: '<p class="url"><i class="fa fa-link"></i>No url found</p>', attribute: "source_html"},
            'locality-scope-of-service': {default: "..please define scope of service", attribute: "scope_of_service"},
            'locality-ancillary-service': {default: "..please define ancillary services", attribute: "ancillary_services"},
            'locality-activities': {default: "..please define ancillary activities", attribute: "activities"},
            'locality-ownership': {default: "..please define ownership status", attribute: "operator_type"},
            'locality-inpatient-service': {default: "..please define number of full time/part time beds", attribute: "inpatient_service"},
            'locality-staff': {default: "..please define full time doctors and full time nurses", attribute: "staff"},
            'other-tags-table': {default: "please use this field to define any additional services available from this location", attribute: null},
        },
        initialize: function () {
            this.listenTo(shared.dispatcher, 'show-locality-detail', this.showDetail);
            this.$sidebar = $('#locality-info');
            this.$completenees = $('.progress-bar');
            this.$otherTagsSection = $('#other-tags-table');
        },
        showDetail: function (parameter) {
            $('.details').hide();
            this.$sidebar.show();
            this.showDefaultInfo();
            this.getInfo(
                parameter['osm_type'], parameter['osm_id']
            );
        },
        showDefaultInfo: function (evt) {
            var self = this;
            $.each(this.attributes_and_element, function (key, value) {
                self.insertIntoElement(key, value['default']);
            })
        },
        getInfo: function (osm_type, osm_id) {
            var self = this;
            $.ajax({
                url: this.url + osm_type + '/' + osm_id + "?output=geojson",
                dataType: 'json',
                success: function (data) {
                    self.showInfo(osm_type, osm_id, data);
                }
            });
        },
        insertIntoElement(id, value) {
            if (value) {
                var $element = $('#' + id);
                if (id === 'uploader') {
                    $element.attr("href", "profile/" + value)
                    value = "@" + value;
                }
                $element.html(value);
            }
        },
        showInfo: function (osm_type, osm_id, data) {
            var self = this;
            var identifier = osm_type + '/' + osm_id;
            var properties = data['properties'];
            var attributes = jQuery.extend({}, properties['attributes']);

            // zoom to map
            var name = 'No Name';
            if (attributes['name']) {
                name = attributes['name'];
            }
            var centroid = properties.centroid['coordinates'];
            attributes['coordinates'] = 'lat: ' + centroid[1] + ', long: ' + centroid[0];
            attributes['changeset_timestamp'] = getDateString(attributes['changeset_timestamp']);
            if (attributes['changeset_user']) {
                attributes['changeset_user'] = attributes['changeset_user'];
            }
            if (properties['completeness']) {
                this.$completenees.attr('style', 'width:' + properties['completeness'] + '%');
                this.$completenees.text(properties['completeness'] + '% Complete');
            }
            if (attributes['staff_doctors'] || attributes['staff_nurses']) {
                var staff = [];
                if (attributes['staff_doctors']) {
                    staff.push("<strong>" + attributes['staff_doctors'] + "</strong> full time doctors");
                    delete attributes['staff_doctors'];
                }
                if (attributes['staff_nurses']) {
                    staff.push("<strong>" + attributes['staff_nurses'] + "</strong> full time nurses");
                    delete attributes['staff_nurses'];
                }
                attributes['staff'] = staff.join(',&nbsp');
            }
            if (attributes['beds'] || attributes['part_time_beds']) {
                var beds = [];
                if (attributes['beds']) {
                    beds.push("<strong>" + attributes['beds'] + "</strong> full time beds");
                    delete attributes['beds'];
                }
                if (attributes['part_time_beds']) {
                    beds.push("<strong>" + attributes['part_time_beds'] + "</strong> part time beds");
                    delete attributes['part_time_beds'];
                }
                attributes['inpatient_service'] = beds.join(',&nbsp');
            }
            $.each(this.attributes_and_element, function (key, value) {
                if (value['attribute']) {
                    self.insertIntoElement(key, attributes[value['attribute']]);
                    delete attributes[value['attribute']];
                }
            });
            var html = '<p class="url"><i class="fa fa-link"></i><a href="https://www.openstreetmap.org/' + identifier + '"';
            html += ' data-toggle="tooltip" title="Data supplied by" target="_blank">OpenStreetMap</a></p>';
            $('.url').html(html);
            $APP.trigger('locality.info', {
                'locality_uuid': identifier,
                'locality_name': name,
                'geom': centroid,
                'zoomto': true
            });

            var geometry = data['geometry'];
            $APP.trigger('map.create-locality-polygon', geometry);

            // SHOW OTHERS INFO
            delete attributes['changeset_id'];
            delete attributes['changeset_version'];
            if (Object.keys(attributes).length >= 1) {
                var otherHtml = '<table>';
                $.each(Object.keys(attributes).sort(), function (index, key) {
                    if (attributes[key]) {
                        otherHtml += '<tr><td>' + key + '</td><td>' + attributes[key] + '</td></tr>';
                    }
                });
                otherHtml += '</table>';
                this.$otherTagsSection.html(otherHtml);
            }
        },

    })
});

