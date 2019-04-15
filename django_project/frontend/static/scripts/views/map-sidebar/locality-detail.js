define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        attributes_and_element: {
            'locality-name': {default: "No Name", attribute: 'name'},
            'last_update': {default: "-", attribute: 'changeset_timestamp'},
            'uploader': {default: "-", attribute: 'changeset_user'},
            'locality-nature-of-facility': {default: "needs information", attribute: 'nature_of_facility'},
            'locality-completeness': {default: "0% Complete", attribute: 'completeness'},
            'locality-coordinates': {default: "lat: n/a, long: n/a", attribute: 'coordinates'},
            'locality-physical-address': {default: "..please update address", attribute: "physical_address"},
            'locality-phone': {default: "..please update phone number", attribute: "phone"},
            'locality-url': {default: '<p class="url"><i class="fa fa-link"></i>No url found</p>', attribute: "source_html"},
            'locality-scope-of-service': {default: "..please define scope of service", attribute: "scope_of_service"},
            'locality-ancillary-service': {default: "..please define ancillary services", attribute: "ancillary_services"},
            'locality-activities': {default: "..please define ancillary activities", attribute: "activities"},
            'locality-ownership': {default: "..please define ownership status", attribute: "ownership"},
            'locality-inpatient-service': {default: "..please define number of full time/part time beds", attribute: "inpatient_service"},
            'locality-staff': {default: "..please define full time doctors and full time nurses", attribute: "staff"},
        },
        initialize: function () {
            this.listenTo(shared.dispatcher, 'show-locality-detail', this.showDetail);
            this.$sidebar = $('#locality-info');
            this.$completenees = $('.progress-bar');
        },
        showDetail: function (parameter) {
            $('.details').hide();
            this.$sidebar.show();
            this.showDefaultInfo();
            this.getInfo(parameter['uuid']);
        },
        showDefaultInfo: function (evt) {
            var self = this;
            $.each(this.attributes_and_element, function (key, value) {
                self.insertIntoElement(key, value['default']);
            })
        },
        getInfo: function (identifire) {
            var self = this;
            $.ajax({
                url: this.url + identifire + "?output=geojson",
                dataType: 'json',
                success: function (data) {
                    self.showInfo(identifire, data);
                }
            });
        },
        insertIntoElement(id, value) {
            if (value) {
                var $element = $('#' + id);
                if (id === 'uploader') {
                    $element.attr("href", "profile/" + value)
                }
                $element.html(value);
            }
        },
        showInfo: function (identifire, data) {
            var self = this;
            var properties = data['properties'];
            var attributes = properties['attributes'];
            attributes['coordinates'] = 'lat: ' + properties.geometry[1] + ', long: ' + properties.geometry[0];
            attributes['changeset_timestamp'] = getDateString(attributes['changeset_timestamp']);
            if (attributes['changeset_user']) {
                attributes['changeset_user'] = "@" + attributes['changeset_user'];
            }
            if (properties['completeness']) {
                this.$completenees.attr('style', 'width:' + properties['completeness'] + '%');
                this.$completenees.text(properties['completeness'] + '% Complete');
            }
            $.each(this.attributes_and_element, function (key, value) {
                self.insertIntoElement(key, attributes[value['attribute']]);
            });
            // zoom to map
            var name = 'No Name';
            if (attributes['name']) {
                name = attributes['name'];
            }
            var html = '<p class="url"><i class="fa fa-link"></i><a href="https://www.openstreetmap.org/' + identifire + '"';
            html += ' data-toggle="tooltip" title="Data supplied by" target="_blank">OpenStreetMap</a></p>';
            $('.url').html(html);
            $APP.trigger('locality.info', {
                'locality_uuid': identifire,
                'locality_name': name,
                'geom': properties.geometry,
                'zoomto': true
            });

            var geometry = data['geometry'];
            $APP.trigger('map.create-locality-polygon', geometry);
        },

    })
});

