/**
 * nlform.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2013, Codrops
 * http://www.codrops.com
 */
;( function( window ) {

    'use strict';

    var document = window.document;

    if (!String.prototype.trim) {
        String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g, '');};
    }

    function NLForm( el ) {
        this.el = el;
        this.fields = [];
        this.fldOpen = -1;
        this._generateS('3');
        this._init();
    }

    NLForm.prototype = {
        _generateS: function(option) {
            var html = [
                'I want to ',
                '<select id="nl-form-1">',
                    //'<option value="1">edit</option>',  // Temporary remove edit option
                    '<option value="3">share</option>',
                '</select>',
                ' this locality'
            ];
            if (option === '3' || option ==='2') {
                html.push(
                    ' via ',
                    '<select id="nl-form-2">',
                        '<option value="1">twitter</option>',
                    '</select>'
                );
            }

            this.el.innerHTML = html.join('');
            $('#nl-form-1').val(option);
            $APP.trigger('locality.show-info-adjust');
        },

        _init : function() {
            var self = this;
            Array.prototype.slice.call( this.el.querySelectorAll( 'select' ) ).forEach( function( el, i ) {
                self.fldOpen++;
                self.fields.push( new NLField( self, el, 'dropdown', self.fldOpen ) );
            } );
        },
        _closeFlds : function() {
            if( this.fldOpen !== -1 ) {
                this.fields[ this.fldOpen ].close();
            }
        },

        _check: function(elem) {
            if ($(elem).attr('id') == 'nl-form-1') {
                var val = $('#nl-form-1').val();
                this._generateS(val);
                this._init();
            }
        }
    };

    function NLField( form, el, type, idx ) {
        this.form = form;
        this.elOriginal = el;
        this.pos = idx;
        this.type = type;
        this._create();
        this._initEvents();
    }

    NLField.prototype = {
        _create : function() {
            if( this.type === 'dropdown' ) {
                this._createDropDown();
            }
        },
        _createDropDown : function() {
            var self = this;
            this.fld = document.createElement( 'div' );
            this.fld.className = 'nl-field nl-dd';
            this.toggle = document.createElement( 'a' );
            this.toggle.innerHTML = this.elOriginal.options[ this.elOriginal.selectedIndex ].innerHTML;
            this.toggle.className = 'nl-field-toggle';
            this.optionsList = document.createElement( 'ul' );
            var ihtml = '';
            Array.prototype.slice.call( this.elOriginal.querySelectorAll( 'option' ) ).forEach( function( el, i ) {
                ihtml += self.elOriginal.selectedIndex === i ? '<li class="nl-dd-checked">' + el.innerHTML + '</li>' : '<li>' + el.innerHTML + '</li>';
                // selected index value
                if( self.elOriginal.selectedIndex === i ) {
                    self.selectedIdx = i;
                }
            } );
            this.optionsList.innerHTML = ihtml;
            this.fld.appendChild( this.toggle );
            this.fld.appendChild( this.optionsList );
            this.elOriginal.parentNode.insertBefore( this.fld, this.elOriginal );
            this.elOriginal.style.display = 'none';
        },
        _initEvents : function() {
            var self = this;
            this.toggle.addEventListener( 'click', function( ev ) { ev.preventDefault(); ev.stopPropagation(); self._open(); } );
            this.toggle.addEventListener( 'touchstart', function( ev ) { ev.preventDefault(); ev.stopPropagation(); self._open(); } );

            if( this.type === 'dropdown' ) {
                var opts = Array.prototype.slice.call( this.optionsList.querySelectorAll( 'li' ) );
                opts.forEach( function( el, i ) {
                    el.addEventListener( 'click', function( ev ) { ev.preventDefault(); self.close( el, opts.indexOf( el ) ); } );
                    el.addEventListener( 'touchstart', function( ev ) { ev.preventDefault(); self.close( el, opts.indexOf( el ) ); } );
                } );
            }

        },
        _open : function() {
            if( this.open ) {
                return false;
            }
            this.open = true;
            this.form.fldOpen = this.pos;
            var self = this;
            this.fld.className += ' nl-field-open';
        },
        close : function( opt, idx ) {
            if( !this.open ) {
                return false;
            }
            this.open = false;
            this.form.fldOpen = -1;
            this.fld.className = this.fld.className.replace(/\b nl-field-open\b/,'');

            if( this.type === 'dropdown' ) {
                if( opt ) {
                    // remove class nl-dd-checked from previous option
                    var selectedopt = this.optionsList.children[ this.selectedIdx ];
                    selectedopt.className = '';
                    opt.className = 'nl-dd-checked';
                    this.toggle.innerHTML = opt.innerHTML;
                    // update selected index value
                    this.selectedIdx = idx;
                    // update original select element´s value
                    this.elOriginal.value = this.elOriginal.children[ this.selectedIdx ].value;
                    this.form._check(this.elOriginal);
                }
            }
        }
    };

    // add to global namespace
    window.NLForm = NLForm;

} )( window );
