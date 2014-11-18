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

        // HARDCODED DOMAIN NAME
        DOMAIN: 'Health',

        _bindInternalEvents: function() {
            var self = this;
            this.$modal.on('hide.bs.modal', function (evt) {
                // remove marker layer from the map
                $APP.trigger('map.remove.point');
            })

            this.$modal.on('get-info', this.getInfo.bind(this));
            this.$modal.on('show-info', this.showInfo.bind(this));
            this.$modal.on('show-edit', this.showEdit.bind(this));

            this.$modal.on('create-new', this.createNewLocality.bind(this));
            this.$modal.on('show-create', this.showCreate.bind(this));
            this.$modal.on('update-coordinates', this.updateCoordinates.bind(this));

            this.$modal_footer.on('click', '.edit', this.showEditForm.bind(this));
            this.$modal_footer.on('click', '.save', this.saveForm.bind(this));
            this.$modal_footer.on('click', '.cancel', this.cancelEdit.bind(this));

            this.$modal_footer.on('click', '.save-create', this.saveCreateForm.bind(this));
            this.$modal_footer.on('click', '.cancel-create', this.cancelCreate.bind(this));

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

        cancelCreate: function(evt) {
            $APP.trigger('map.cancel.edit');
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
                $APP.trigger('map.show.point', {'geom':[data.geom[1], data.geom[0]]});
            });
        },

        showEdit: function(evt, payload) {
            this.$modal_body.html(payload.data);
            this.$modal_footer.html([
                '<button type="button" class="btn btn-default cancel">Cancel</button>',
                '<button type="button" class="btn btn-warning save">Save changes</button>'
            ].join(''))

            // 'remove' modal window backdrop
            $('.modal-backdrop').css('position', 'relative');
        },

        showCreate: function(evt, payload) {
            this.$modal_body.html(payload.data);
            if (payload.geom) {
                $('#id_lon').val(payload.geom[1]);
                $('#id_lat').val(payload.geom[0]);
            }

            this.$modal_footer.html([
                '<button type="button" class="btn btn-default cancel-create">Cancel</button>',
                '<button type="button" class="btn btn-warning save-create">Create</button>'
            ].join(''))
            // show modal create
            this.$modal.modal('show');

            // 'remove' modal window backdrop
            $('.modal-backdrop').css('position', 'relative');
        },

        showEditForm: function(evt) {
            var self = this;
            $.get('/localities/'+this.locality_id+'/form', function (data) {
                self.$modal.trigger('show-edit', {'data':data});
            });
        },

        createNewLocality: function(evt, payload) {
            var self = this;
            $.get('/localities/form/'+this.DOMAIN, function (data) {
                $APP.trigger('map.show.point', {'geom':[payload.data.lat, payload.data.lng]});
                self.$modal.trigger('show-create', {'data':data, 'geom':[payload.data.lat, payload.data.lng] });
            });
        },

        saveForm: function(evt) {
            var self = this;
            var form = this.$modal_body.find('form');
            var latlng = [$('#id_lat').val(), $('#id_lon').val()];
            var data = form.serializeArray();

            $.ajax('/localities/'+this.locality_id+'/form', {
                'type': 'POST',
                'data': data,
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

        saveCreateForm: function(evt) {
            var self = this;
            var form = this.$modal_body.find('form');

            $.ajax('/localities/form/'+this.DOMAIN, {
                'type': 'POST',
                'data': form.serializeArray(),
                'success': function (data, status, xhr) {
                    // try to parse data as an integer (ID)
                    var new_loc_id = parseInt(data, 10);
                    var latlng = [$('#id_lat').val(), $('#id_lon').val()];
                    if (isNaN(new_loc_id)) {
                        // there were some form processing errors
                        self.$modal.trigger('show-create', {'data': data});
                    } else {
                        // hide form...
                        // trigger create cleanup
                        self.$modal.modal('hide');
                        $APP.trigger('locality.created', {
                            'loc_id': new_loc_id, 'latlng': latlng
                        });
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

            $APP.on('locality.new.create', function (evt, payload) {
                self.$modal.trigger('create-new', payload);
            });
        }
    }

// return module
return module;
}());