define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        tag_and_default: {
            'name': 'No Name',
            'amenity': 'needs information',
            'completeness': '0% Complete',
            'addr_full': '..please update address',
            'contact_number': '..please update phone number',
            'source_html': 'No url found',
            'operator_type': '..please define ownership status',
            'notes': '..please define notes hospitalisation and outpatient consultation',
            'opening_hours': '..please define operating hours',
            'tag': '..please add comma separated tags'
        },
        initialize: function (definitions) {
            this.$completenees = $('.progress-bar');
            this.$otherTagsSection = $('#other-tags-table');
            this.definitions = definitions;
        },
        showDefaultInfo: function (evt) {
            /** Showing default information, especially for empty value **/
            var self = this;
            $('.data').html('-');
            $.each(this.tag_and_default, function (key, value) {
                self.insertIntoElement(key, value, true);
            })
        },
        insertIntoElement(id, value, isDefault) {
            /** Insert value into element **/
            if (value) {
                var $element = $($('*[data-tag="' + id + '"]').find('.data,.uneditable-data'));
                if ($element.length === 0) {
                    return false;
                }
                if (id === 'changeset_user') {
                    $element.attr("href", "profile/" + value);
                    value = "@" + value;
                }
                $element.html(value);

                // use class empty if it is default
                if (isDefault) {
                    $element.addClass('empty');
                } else {
                    $element.removeClass('empty');
                }
            }
            return true;
        },
        showTags: function (attributes) {
            // SHOW OTHERS INFO
            var otherHtml = '';
            var self = this;
            this.$otherTagsSection.html('');
            $.each(Object.keys(this.definitions).sort(), function (index, key) {
                var $element = $('*[data-tag="' + key + '"]');
                var definition = self.definitions[key];
                var description = definition['description'];
                if (definition['required']) {
                    description = '[REQUIRED] ' + definition['description'];
                }
                if ($element.length === 0) {
                    var value = '';
                    if (attributes[key]) {
                        value = attributes[key];
                        delete attributes[key];
                    }
                    otherHtml += '<tr data-tag="' + key + '"  data-hasvalue="' + (value !== '') + '" data-required="' + definition['required'] + '">' +
                        '<td class="tag-key">' + key + ' <i class="fa fa-info-circle" aria-hidden="true" title="' + description + '"></i></td>' +
                        '<td><div class="data">' + value + '</div></td>' +
                        '</tr>';
                }
            });
            if (Object.keys(attributes).length >= 1) {
                $.each(Object.keys(attributes).sort(), function (index, key) {
                    if (attributes[key]) {
                        if (!self.insertIntoElement(key, attributes[key])) {
                            otherHtml += '<tr data-tag="' + key + '">' +
                                '<td>' + key + '</td>' +
                                '<td><div class="data">' + attributes[key] + '</div></td>' +
                                '</tr>';

                        }
                    }
                });
            }
            if (otherHtml) {
                this.$otherTagsSection.html('<table>' + otherHtml + '</table>');
            }
        },
        showInfo: function (osm_type, osm_id, data) {
            /** SHOWING INFORMATION TAGS OF HEALHTSITE **/
            var identifier = null;
            if (osm_type) {
                identifier = osm_type + '/' + osm_id;
            }
            var properties = data['properties'];
            var attributes = jQuery.extend({}, properties['attributes']);

            // name of attribute
            var name = 'No Name';
            if (attributes['name']) {
                name = attributes['name'];
            }
            var centroid = properties.centroid['coordinates'];
            attributes['latitude'] = centroid[1];
            attributes['longitude'] = centroid[0];
            attributes['changeset_timestamp'] = getDateString(attributes['changeset_timestamp']);
            if (properties['completeness']) {
                this.$completenees.attr('style', 'width:' + properties['completeness'] + '%');
                this.$completenees.text(properties['completeness'] + '% Complete');
            }
            // source url
            if (identifier) {
                var html = '<a href="https://www.openstreetmap.org/' + identifier + '"';
                html += ' data-toggle="tooltip" title="Data supplied by" target="_blank">OpenStreetMap</a>';
                attributes['source_html'] = html;
            }

            shared.dispatcher.trigger('locality.info', {
                'locality_uuid': identifier,
                'locality_name': name,
                'geom': centroid,
                'zoomto': true
            });

            var geometry = data['geometry'];
            shared.dispatcher.trigger('map.create-locality-polygon', geometry);

            delete attributes['changeset_id'];
            delete attributes['changeset_version'];
            this.showTags(attributes);
        },

    })
});

