define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        tag_and_default: {
            'name': 'No Name',
            'amenity': 'needs information',
            'completeness': '0% Complete',
            'physical_address': '..please update address',
            'phone': '..please update phone number',
            'source_html': 'No url found',
            'operator_type': '..please define ownership status',
            'notes': '..please define notes hospitalisation and outpatient consultation',
            'opening_hours': '..please define operating hours',
            'tag': '..please add comma separated tags'
        },
        initialize: function () {
            this.$completenees = $('.progress-bar');
            this.$otherTagsSection = $('#other-tags-table');
        },
        showDefaultInfo: function (evt) {
            var self = this;
            $('.data').html('-');
            $.each(this.tag_and_default, function (key, value) {
                self.insertIntoElement(key, value, true);
            })
        },
        insertIntoElement(id, value, isDefault) {
            if (value) {
                var $element = $($('*[data-tag="' + id + '"]').find('.data'));
                if ($element.length === 0) {
                    return false;
                }
                if (id === 'changeset_user') {
                    $element.attr("href", "profile/" + value);
                    value = "@" + value;
                }
                $element.html(value);
                if (isDefault) {
                    $element.addClass('empty');
                } else {
                    $element.removeClass('empty');
                }
            }
            return true;
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
            attributes['latitude'] = centroid[1];
            attributes['longitude'] = centroid[0];
            attributes['changeset_timestamp'] = getDateString(attributes['changeset_timestamp']);
            if (attributes['changeset_user']) {
                attributes['changeset_user'] = attributes['changeset_user'];
            }
            if (properties['completeness']) {
                this.$completenees.attr('style', 'width:' + properties['completeness'] + '%');
                this.$completenees.text(properties['completeness'] + '% Complete');
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
            // source url
            var html = '<a href="https://www.openstreetmap.org/' + identifier + '"';
            html += ' data-toggle="tooltip" title="Data supplied by" target="_blank">OpenStreetMap</a>';
            attributes['source_html'] = html;

            $APP.trigger('locality.info', {
                'locality_uuid': identifier,
                'locality_name': name,
                'geom': centroid,
                'zoomto': true
            });

            var geometry = data['geometry'];
            $APP.trigger('map.create-locality-polygon', geometry);

            delete attributes['changeset_id'];
            delete attributes['changeset_version'];
            // SHOW OTHERS INFO
            var otherHtml = '';
            if (Object.keys(attributes).length >= 1) {
                $.each(Object.keys(attributes).sort(), function (index, key) {
                    if (attributes[key]) {
                        if (!self.insertIntoElement(key, attributes[key])) {
                            otherHtml += '<tr><td>' + key + '</td><td>' + attributes[key] + '</td></tr>';

                        }
                    }
                });
            }
            if (otherHtml) {
                otherHtml += '';
                this.$otherTagsSection.html('<table>' + otherHtml + '</table>');
            }
        },

    })
});

