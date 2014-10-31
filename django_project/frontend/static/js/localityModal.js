window.LocalityModal = (function () {
    "use strict";
    // private variables and functions

    // constructor
    var module = function () {

        this.$modal = $(this.template).modal({'backdrop': 'static', 'show':false, 'keyboard': false});
        this.$modal_title = this.$modal.find('.modal-title');
        this.$modal_body = this.$modal.find('.modal-body');
        this.$modal_footer = this.$modal.find('.modal-footer');

        this.$modal.appendTo('body');

        this._bindExternalEvents();
        this._bindInternalEvents();

    };

    // prototype
    module.prototype = {
        constructor: module,
        template : [
            '<div id="localityModal" class="modal fade">',
            '<div class="modal-dialog">',
            '<div class="modal-content">',
                '<div class="modal-header">',
                    '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>',
                    '<h4 class="modal-title">Modal title</h4>',
                '</div>',
                '<div class="modal-body">',
                '</div>',
                '<div class="modal-footer">',
                '</div>',
            '</div>',
            '</div>',
            '</div>'
        ].join(''),

        _bindInternalEvents: function() {
            var self = this;
            this.$modal.on('hidden.bs.modal', function (evt) {
                // remove marker layer from the map
                $APP.trigger('map.remove.point');
            })

            this.$modal.on('get-info', this.getInfo.bind(this));
            this.$modal.on('show-info', this.showInfo.bind(this));
            this.$modal.on('show-edit', this.showEdit.bind(this));
            this.$modal.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$modal_footer.on('click', '.edit', this.showEditForm.bind(this));
            this.$modal_footer.on('click', '.save', this.saveForm.bind(this));
            this.$modal_footer.on('click', '.cancel', this.cancelEdit.bind(this));

            this.$modal_footer.on('click', '.close-modal', function (evt) {
                self.$modal.modal('hide');
            });
        },

        updateCoordinates: function (evt, payload) {
            // set new values
            $('#id_lon').val(payload.latlng.lng);
            $('#id_lat').val(payload.latlng.lat);
        },

        cancelEdit: function(evt) {
            $APP.trigger('map.cancel.edit');
            // 'show' modal window backdrop
            this.showInfo();
        },


        showInfo: function(evt) {
            $('.modal-backdrop').css('position', 'absolute');
            this.$modal_body.html(this.locality_data.repr);
            this.$modal.modal('show');

            // buttons
            this.$modal_footer.html([
                '<button type="button" class="btn btn-default close-modal">Close</button>',
                '<button type="button" class="btn btn-primary edit">Edit Locality</button>'
            ].join(''))
        },

        getInfo: function(evt) {
            var self = this;
            $.getJSON('/localities/' + this.locality_id, function (data) {
                self.locality_data = data;
                self.$modal.trigger('show-info');
                // show selected point on the map
                $APP.trigger('map.show.point', data);
            });
        },

        showEdit: function(evt, payload) {
            this.$modal_body.html(payload.data);
            var edit_action = this.$modal_footer.find('.edit');
            edit_action.toggleClass('edit btn-warning save').text('Save Changes');

            var close_action = this.$modal_footer.find('.close-modal');
            close_action.toggleClass('close-modal cancel').text('Cancel');

            // 'remove' modal window backdrop
            $('.modal-backdrop').css('position', 'relative');
        },

        showEditForm: function(evt) {
            var self = this;
            $.get('/localities/'+this.locality_id+'/form', function (data) {
                self.$modal.trigger('show-edit', {'data':data});
            });
        },

        showCreateForm: function(evt) {
            var self = this;
            $.get('/localities/'+this.locality_id+'/form', function (data) {
                self.$modal.trigger('show-edit', {'data':data});
            });
        },

        saveForm: function(evt) {
            var self = this;
            var form = this.$modal_body.find('form');

            $.ajax('/localities/'+this.locality_id+'/form', {
                'type': 'POST',
                'data': form.serializeArray(),
                'success': function (data, status, xhr) {
                    if (data !== 'OK') {
                        // there were some form processing errors
                        self.$modal.trigger('show-edit', {'data': data});
                    } else {
                        self.$modal.trigger('get-info');
                    }
                },
                'error': function (xhr, status, error) {
                    console.log(xhr, status, error);
                }
            })
        },

        _bindExternalEvents: function () {
            var self = this;

            $APP.on('locality.map.click', function (evt, payload) {
                self.locality_id = payload.locality_id;
                self.$modal.trigger('get-info');
            });
            $APP.on('locality.map.move', function (evt, payload) {
                self.$modal.trigger('update-coordinates', payload);
            });

            $APP.on('locality.new.save', function (evt, payload) {

            }
        }
    }

// return module
return module;
}());