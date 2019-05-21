define([
    'backbone',
    'jquery',
    'static/scripts/views/map-sidebar/healthsite-detail/detail.js',
    'static/scripts/views/map-sidebar/healthsite-detail/form.js'], function (Backbone, $, Detail, Form) {
    return Backbone.View.extend({
        url: '/api/v2/facilities/',
        initialize: function () {
            this.$el = $('#locality-info');
            this.listenTo(shared.dispatcher, 'show-locality-detail', this.showDetail);
            this.$sidebar = $('#locality-info');
            this.$editButton = $('#edit-healthsite');
            this.$createButton = $('#create-healthsite');
            this.$saveButton = $('#save-healthsite');
            this.$cancelButton = $('#cancel-healthsite');
            this.toMapMode();
            this.detail = new Detail();
            this.form = new Form();

            // init event
            var self = this;
            this.$editButton.click(function () {
                self.toEditMode();
            });
            this.$createButton.click(function () {
                self.toCreateMode();
            });
            this.$saveButton.click(function () {
                self.toSaveMode();
            });
            this.$cancelButton.click(function () {
                self.toDetailMode();
            });
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
            $.ajax({
                url: this.url + osm_type + '/' + osm_id + "?output=geojson",
                dataType: 'json',
                success: function (data) {
                    self.detail.showInfo(osm_type, osm_id, data);
                    self.toDetailMode();
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
        },
        toFormMode: function () {
            /** This is when form show **/
            this.$editButton.hide();
            this.$createButton.hide();
            this.$saveButton.show();
            this.$cancelButton.show();
            this.$el.find('.data').hide();
            this.$el.find('.input').show();
        },
        toCreateMode: function () {
            /** This is when edit form enabled **/
            /** Asking form to render in default inputs **/
            this.toFormMode()
        },
        toEditMode: function () {
            /** This is when edit form enabled **/
            /** Giving form current data, as default data on inputs **/
            this.toFormMode()
        },
        toSaveMode: function () {
            /** Asking form to push the data on form **/
        }
    })
});

