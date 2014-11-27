window.LocalityModal = (function () {
    "use strict";
    // private variables and functions

    // constructor
    var module = function () {

        this.$modal = $('#sidebar-info');
        this.$modal.html(this.template);
        this.$modal_head = this.$modal.find('.sidebar-info-header');
        this.$modal_body = this.$modal.find('.sidebar-info-body');
        this.$modal_footer = this.$modal.find('.sidebar-info-footer');

        this._bindExternalEvents();
        this._bindInternalEvents();

    };

    // prototype
    module.prototype = {
        constructor: module,
        template : [
            '<div class="sidebar-info-header"></div>',
            '<div class="sidebar-info-body">Click a marker on the map to load locality info</div>',
            '<div class="sidebar-info-footer"></div>',
        ].join(''),

        _bindInternalEvents: function() {
            var self = this;
            this.$modal.on('hide.bs.modal', function (evt) {
                // remove marker layer from the map
                $APP.trigger('map.remove.point');
            })

            this.$modal.on('handle-xhr-error', this.handleXHRError.bind(this));

            this.$modal.on('get-info', this.getInfo.bind(this));
            this.$modal.on('show-info', this.showInfo.bind(this));
            this.$modal.on('show-info-adjust', this.setInfoWindowHeight.bind(this));
            this.$modal.on('show-edit', this.showEdit.bind(this));
    
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
            });


            this.$modal_head.on('mouseover', '.label-status', function() {
                self.$modal_head.find('.modal-info-information').addClass('modal-info-expanded').animate({height: "100px"}, 500);
            });

            this.$modal_head.on('mouseout', '.label-status', function() {
                self.$modal_head.find('.modal-info-information').animate({height: "1px"}, 100).removeClass('modal-info-expanded');
            });
        },

        handleXHRError: function(evt, payload) {
            var xhr = payload['xhr'];

            // show error notification
            if (xhr.status === 403 ) {
                alert('Please login before continuing!');
            } else {
                alert('Error processing XHR request!');
            }
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

        showInfo: function(evt) {
            var modal_head = [
                '<div class="modal-info-status">',
                    'This information is considered ',
                    '<span class="label label-success">current</span>. ',
                    '<span class="label-status">Why</span>?',
                    //'<a class="close-modal pull-right"><i class="mdi-navigation-close"></i></a>',
                '</div>',
                '<div class="modal-info-information">',
                    '<p>- It was manualy verified by trusted user</p>',
                    '<p>- It was been verified using social harvesting</p>',
                    '<p>- 13 people have verfified its existance in last 3 months</p>',
                '</div>',
            ].join('');
            // placeholder for info quality
            //this.$modal_head.html(modal_head);
            this.$modal_body.html(this.locality_data.repr);
            this.$modal_footer.html([
                '<span id="nl-form" class="nl-form"></span>',
                '<button type="button" id="nl-execute" class="btn btn-xs btn-success nl-execute"> GO <i class="mdi-av-play-arrow"></i></button>',
            ].join(''));
            var form = new NLForm( document.getElementById( 'nl-form' ) );
            $('#sidebar').addClass('active');
            $('#sidebar-helper').addClass('active');
            $('#collapseInfo').collapse('show');
            this.$modal.trigger('show-info-adjust');
        },

        setInfoWindowHeight: function() {
            var nlfH =  this.$modal_footer.height();
            this.$modal_body.height($(window).height() - this.$modal_body.offset().top - nlfH);
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

            this.$modal_body.find('input:text').filter(function() { return $(this).val() == ""; }).each(function() {
                $(this).parents('.form-group').detach().appendTo('#empty-form-tab');
            });

        },


        showEditForm: function(evt) {
            var self = this;
            $.get('/localities/'+this.locality_id+'/form', function (data) {
                self.$modal.trigger('show-edit', {'data':data});
                // show red-marker on the map
                $APP.trigger('locality.edit', {'geom':[self.locality_data.geom[1], self.locality_data.geom[0]]});
            }).fail(function(xhr, status, error) {
                self.$modal.trigger('handle-xhr-error', {'xhr': xhr});
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
                    self.$modal.trigger('handle-xhr-error', {'xhr': xhr});
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

            });
            $APP.on('locality.show-info-adjust', function(evt, payload) {
                self.$modal.trigger('show-info-adjust');
        }
    }

// return module
return module;
}());
