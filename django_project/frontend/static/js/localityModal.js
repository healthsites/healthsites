window.LocalityModal = (function () {
    "use strict";
    // private variables and functions

    // constructor
    var module = function () {

        this.$modal = $(this.template).modal({'backdrop': 'static', 'show':false, 'keyboard': false});
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
                '<div class="modal-body modal-body-info">',
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

            this.$modal_footer.on('click', '.nl-execute', function() {
                var val = $('#nl-form-1').val();
                if (val === '1') {
                    self.showEditForm.call(self);
                }
                if (val === '2') {
                    var val2 = $('#nl-form-2').val();
                    if (val2 === '1') {
                        var loc = 'https://twitter.com/intent/tweet?text=See%20'+self.locality_data.values.name+'.%20Please%20validate&url=http://healthsites.io/'+ self.locality_id +'/';
                        self.sendTweet(loc);
                    }
                }
                if (val === '3') {
                    var val2 = $('#nl-form-2').val();
                    if (val2 === '1') {
                        var loc = 'https://twitter.com/intent/tweet?text=See%20'+self.locality_data.values.name+'&url=http://healthsites.io/'+ self.locality_id +'/';
                        self.sendTweet(loc);
                    }
                }
            })


            this.$modal_footer.on('click', '.save-create', this.saveCreateForm.bind(this));
            this.$modal_footer.on('click', '.cancel-create', this.cancelCreate.bind(this));

            this.$modal_body.on('click', '.close-modal', function (evt) {
                self.$modal.modal('hide');
            });

            this.$modal_body.on('mouseover', '.label-status', function() {
                self.$modal_body.find('.modal-info-information').addClass('modal-info-expanded').animate({height: "100px"}, 500);
            });

            this.$modal_body.on('mouseout', '.label-status', function() {
                self.$modal_body.find('.modal-info-information').animate({height: "1px"}, 100).removeClass('modal-info-expanded');
            });

            this.$modal_body.on('click', '.mdi-social-share', function() {
                self.$modal_body.find('.modal-info-social').animate({width: "115px"}, 500);
            });
        },

        updateCoordinates: function (evt, payload) {
            // set new values
            $('#id_lon').val(payload.latlng.lng);
            $('#id_lat').val(payload.latlng.lat);
        },

        sendTweet: function(text) {
            var windowOptions = 'scrollbars=yes,resizable=yes,toolbar=no,location=yes';
            var width = 550;
            var height = 420;
            var winHeight = screen.height;
            var winWidth = screen.width;
            var left = Math.round((winWidth / 2) - (width / 2));
            var top = 0;
            if (winHeight > height) {
                top = Math.round((winHeight / 2) - (height / 2));
            }
            window.open(text, 'intent', windowOptions + ',width=' + width + ',height=' + height + ',left=' + left + ',top=' + top);
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
            var modal_head = [
                '<div class="modal-info-status">',
                    'This information is considered ',
                    '<span class="label label-success">current</span>. ',
                    '<span class="label-status">Why</span>?',
                    '<a class="close-modal pull-right"><i class="mdi-navigation-close"></i> Close</a>',
                '</div>',
                '<div class="modal-info-information">',
                    '<p>- It was manualy verified by trusted user</p>',
                    '<p>- It was been verified using social harvesting</p>',
                    '<p>- 13 people have verfified its existance in last 3 months</p>',
                '</div>',
            ].join('');
            this.$modal_body.html(modal_head);
            this.$modal_body.append(this.locality_data.repr);
            this.$modal.modal('show');

            // buttons
            /*this.$modal_footer.html([
                '<button type="button" class="btn btn-default close-modal"><i class="mdi-navigation-close"></i> Close</button>',
                '<button type="button" class="btn btn-success"><i class="mdi-action-thumb-up"></i> Verify</button>',
                '<button type="button" class="btn btn-primary edit"><i class="mdi-content-create"></i> Edit Locality</button>'
            ].join(''))
            */
            this.$modal_footer.html([
                '<span id="nl-form" class="nl-form"></span>',
                '<button type="button" id="nl-execute" class="btn btn-xs btn-success nl-execute"> GO <i class="mdi-av-play-arrow"></i></button>',
            ].join(''));
            var form = new NLForm( document.getElementById( 'nl-form' ) );
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

            this.$modal_body.find('input:text').filter(function() { return $(this).val() == ""; }).each(function() {
                $(this).parents('.form-group').detach().appendTo('#empty-form-tab');
            });
            $.material.init();

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
                        $APP.trigger('map.update-maker.location', {'latlng': latlng});
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
