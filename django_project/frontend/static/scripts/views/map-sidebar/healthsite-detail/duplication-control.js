define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        default: function () {
            $('#duplication-modal').modal('show');
            $('.duplication-content').hide();
            var self = this;
            this.$el = $('#duplication-modal');
            $('#comparison-mode button').click(function () {
                $('#comparison-mode button').removeClass('btn-primary');
                $('#comparison-mode button').addClass('btn-default');
                $(this).addClass('btn-primary');
                self.changeMode($(this).html());
            })
        },
        changeMode: function (mode) {
            var self = this;
            $('.original,.duplicate').removeClass('disabled');
            var $oriIndicator = $('#original-indicator');
            var $dupIndicator = $('#duplicate-indicator');

            // render data as content
            this.addData($('#original-content'), this.originalData);

            self.selectedData = null;
            self.osmID = self.originalData['properties']['osm_id'];
            self.mode = mode;
            switch (mode) {
                case "Yes add this":
                    $('.original').addClass('disabled');
                    $oriIndicator.html('Keep this');
                    $dupIndicator.html('Create this as new facility');
                    self.selectedData = self.duplicationData;
                    self.osmID = null;
                    break;
                case "Continue editing":
                    $('.original').addClass('disabled');
                    $oriIndicator.html('Keep this');
                    $dupIndicator.html('Keep editing this new facility');
                    self.selectedData = self.duplicationData;
                    self.osmID = null;
                    break;
                case "Discard and edit original":
                    $('.duplicate').addClass('disabled');
                    $oriIndicator.html('Edit this');
                    $dupIndicator.html('Discard this new facility');
                    self.selectedData = self.originalData;
                    self.osmID = self.originalData['properties']['osm_id'];
                    break;
                case "Update attributes of original":
                    $('.duplicate').addClass('disabled');
                    $oriIndicator.html('Edit this with new facility attributes');
                    $dupIndicator.html('Discard this new facility');
                    self.selectedData = $.extend({}, self.duplicationData);
                    $.each(self.originalData['properties']['attributes'], function (key, value) {
                        console.log(key);
                        if (!self.selectedData['properties']['attributes'][key]) {
                            self.selectedData['properties']['attributes'][key] = value;
                        }
                    });
                    self.osmID = self.originalData['properties']['osm_id'];
                    self.addData($('#original-content'), self.selectedData);
                    break;
            }
        },
        duplicationMoreThanOne: function () {
            this.default();
            $('#more-than-one').show();
        },
        addContent: function ($wrapper, key, value) {
            if (!value) {
                return;
            }
            var html = '<tr>';
            html += '<td>' + key + '</td>';
            if (Array.isArray(value)) {
                value = value.join(', ')
            }
            html += '<td>' + value + '</td>';
            html += '</tr>';
            $wrapper.append(html)
        },
        addData: function ($ontent, input) {
            // add original content
            var self = this;
            $ontent.html('<table style="width:100%;"></table>');
            var $table = $ontent.find('table');
            var data = $.extend({}, input);
            this.addContent($table, 'lat', data['geometry']['coordinates'][1]);
            this.addContent($table, 'lon', data['geometry']['coordinates'][0]);
            var fixedOrder = ['name', 'amenity', 'healthcare', 'healthcare_amenity_type'];
            $.each(fixedOrder, function (index, value) {
                self.addContent($table, value, data['properties']['attributes'][value]);
            });
            Object.keys(data['properties']['attributes']).sort().forEach(function (key) {
                if (fixedOrder.indexOf(key) === -1) {
                    self.addContent($table, key, data['properties']['attributes'][key]);
                }
            });
        },
        showDuplication: function (originalData, duplicationData, applyFunction) {
            this.originalData = originalData;
            this.duplicationData = duplicationData;

            var self = this;
            this.default();
            $('#comparison').show();
            if (!originalData) {
                $('#original-content').html('this original data not found');
                return;
            }
            var originalTitle = "Original record with osm : " + originalData['properties']['osm_id'];
            $('#original-title').html(originalTitle);

            // render data as content
            self.addData($('#original-content'), originalData);
            self.addData($('#duplicate-content'), duplicationData);

            this.changeMode($('#comparison-mode button.btn-primary').html());

            $('#duplication-apply').off('click');
            $('#duplication-apply').click(function () {
                applyFunction(self.selectedData, self.osmID, self.mode);
                $('#duplication-modal').modal('hide');
            })

        },
    })
});

