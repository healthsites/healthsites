/**
 * Created by meomancer on 18/02/16.
 */
function mapcount() {
    var v_width = $(window).width();
    var v_height = $(window).height();
    var s_height = $('.nav-searchbar').height();
    if ($('.nav-searchbar').is(":visible")) {
        var h_height = $('.masthead').height() + s_height;
    }
    else {
        var h_height = $('.masthead').height();
    }
    var s_width = $('.location-info').width();
    var r_height = v_height - h_height;
    if (v_width <= 991) {
        var pad = r_height / 2;
        $('.location-info').css('margin-top', h_height + pad);
        $('.map-page #map').css('top', h_height);
        $('#map, #map-home').css('height', pad);
        $('#map, #map-home').css('width', v_width);

        //mobile country search
        $('.select-country input').focusin(function () {
            $('body').addClass('search-focus');
        });
        $('.select-country input').focusout(function () {
            $('body').removeClass('search-focus');
        });

    }
    else {
        if ($('.select-country').length > 0) {
            var c_height = $('.country-data').css('height');
        }
        $('.location-info').css('margin-top', h_height);
        $('.map-page #map').css('height', v_height - h_height);
        $('.map-page #map').css('width', v_width - s_width);
        $('.map-page #map').css('top', h_height);
        $('body').removeClass('search-focus');
        $('#map, #map-home').css('height', c_height);
    }
}

(function ($) {
    $.cookieBar = function (options, val) {
        if (options == 'cookies') {
            var doReturn = 'cookies';
        } else if (options == 'set') {
            var doReturn = 'set';
        } else {
            var doReturn = false;
        }
        var defaults = {
            message: 'We use cookies to track usage and preferences.', //Message displayed on bar
            acceptButton: true, //Set to true to show accept/enable button
            acceptText: 'I Understand', //Text on accept/enable button
            acceptFunction: function (cookieValue) {
                if (cookieValue != 'enabled' && cookieValue != 'accepted') window.location = window.location.href;
            }, //Function to run after accept
            declineButton: false, //Set to true to show decline/disable button
            declineText: 'Disable Cookies', //Text on decline/disable button
            declineFunction: function (cookieValue) {
                if (cookieValue == 'enabled' || cookieValue == 'accepted') window.location = window.location.href;
            }, //Function to run after decline
            policyButton: false, //Set to true to show Privacy Policy button
            policyText: 'Privacy Policy', //Text on Privacy Policy button
            policyURL: '/privacy-policy/', //URL of Privacy Policy
            autoEnable: true, //Set to true for cookies to be accepted automatically. Banner still shows
            acceptOnContinue: false, //Set to true to accept cookies when visitor moves to another page
            acceptOnScroll: false, //Set to true to accept cookies when visitor scrolls X pixels up or down
            acceptAnyClick: false, //Set to true to accept cookies when visitor clicks anywhere on the page
            expireDays: 365, //Number of days for cookieBar cookie to be stored for
            renewOnVisit: false, //Renew the cookie upon revisit to website
            forceShow: true, //Force cookieBar to show regardless of user cookie preference
            effect: 'slide', //Options: slide, fade, hide
            element: 'body', //Element to append/prepend cookieBar to. Remember "." for class or "#" for id.
            append: false, //Set to true for cookieBar HTML to be placed at base of website. Actual position may change according to CSS
            fixed: false, //Set to true to add the class "fixed" to the cookie bar. Default CSS should fix the position
            bottom: false, //Force CSS when fixed, so bar appears at bottom of website
            zindex: '', //Can be set in CSS, although some may prefer to set here
            domain: String(window.location.hostname), //Location of privacy policy
            referrer: String(document.referrer) //Where visitor has come from
        };
        var options = $.extend(defaults, options);

        //Sets expiration date for cookie
        var expireDate = new Date();
        expireDate.setTime(expireDate.getTime() + (options.expireDays * 86400000));
        expireDate = expireDate.toGMTString();

        var cookieEntry = 'cb-enabled={value}; expires=' + expireDate + '; path=/';

        //Retrieves current cookie preference
        var i, cookieValue = '', aCookie, aCookies = document.cookie.split('; ');
        for (i = 0; i < aCookies.length; i++) {
            aCookie = aCookies[i].split('=');
            if (aCookie[0] == 'cb-enabled') {
                cookieValue = aCookie[1];
            }
        }
        //Sets up default cookie preference if not already set
        if (cookieValue == '' && doReturn != 'cookies' && options.autoEnable) {
            cookieValue = 'enabled';
            document.cookie = cookieEntry.replace('{value}', 'enabled');
        } else if ((cookieValue == 'accepted' || cookieValue == 'declined') && doReturn != 'cookies' && options.renewOnVisit) {
            document.cookie = cookieEntry.replace('{value}', cookieValue);
        }
        if (options.acceptOnContinue) {
            if (options.referrer.indexOf(options.domain) >= 0 && String(window.location.href).indexOf(options.policyURL) == -1 && doReturn != 'cookies' && doReturn != 'set' && cookieValue != 'accepted' && cookieValue != 'declined') {
                doReturn = 'set';
                val = 'accepted';
            }
        }
        if (doReturn == 'cookies') {
            //Returns true if cookies are enabled, false otherwise
            if (cookieValue == 'enabled' || cookieValue == 'accepted') {
                return true;
            } else {
                return false;
            }
        } else if (doReturn == 'set' && (val == 'accepted' || val == 'declined')) {
            //Sets value of cookie to 'accepted' or 'declined'
            document.cookie = cookieEntry.replace('{value}', val);
            if (val == 'accepted') {
                return true;
            } else {
                return false;
            }
        } else {
            //Sets up enable/accept button if required
            var message = options.message.replace('{policy_url}', options.policyURL);

            if (options.acceptButton) {
                var acceptButton = '<a href="" class="cb-enable">' + options.acceptText + '</a>';
            } else {
                var acceptButton = '';
            }
            //Sets up disable/decline button if required
            if (options.declineButton) {
                var declineButton = '<a href="" class="cb-disable">' + options.declineText + '</a>';
            } else {
                var declineButton = '';
            }
            //Sets up privacy policy button if required
            if (options.policyButton) {
                var policyButton = '<a href="' + options.policyURL + '" class="cb-policy">' + options.policyText + '</a>';
            } else {
                var policyButton = '';
            }
            //Whether to add "fixed" class to cookie bar
            if (options.fixed) {
                if (options.bottom) {
                    var fixed = ' class="fixed bottom"';
                } else {
                    var fixed = ' class="fixed"';
                }
            } else {
                var fixed = '';
            }
            if (options.zindex != '') {
                var zindex = ' style="z-index:' + options.zindex + ';"';
            } else {
                var zindex = '';
            }

            //Displays the cookie bar if arguments met
            if (options.forceShow || cookieValue == 'enabled' || cookieValue == '') {
                if (options.append) {
                    $(options.element).append('<div id="cookie-bar"' + fixed + zindex + '><p>' + message + acceptButton + declineButton + policyButton + '</p></div>');
                } else {
                    $(options.element).prepend('<div id="cookie-bar"' + fixed + zindex + '><p>' + message + acceptButton + declineButton + policyButton + '</p></div>');
                }
				$(options.element).addClass('cookiebar-enabled');
            }

            var removeBar = function (func) {
                if (options.acceptOnScroll) $(document).off('scroll');
                if (typeof(func) === 'function') func(cookieValue);
                if (options.effect == 'slide') {
                    $('#cookie-bar').slideUp(300, function () {
                        $('#cookie-bar').remove();
                    });
                } else if (options.effect == 'fade') {
                    $('#cookie-bar').fadeOut(300, function () {
                        $('#cookie-bar').remove();
                    });
                } else {
                    $('#cookie-bar').hide(0, function () {
                        $('#cookie-bar').remove();
                    });
                }
                $(document).unbind('click', anyClick);
				$(options.element).removeClass('cookiebar-enabled');
				policyshow();
            };
            var cookieAccept = function () {
                document.cookie = cookieEntry.replace('{value}', 'accepted');
                removeBar(options.acceptFunction);
            };
            var cookieDecline = function () {
                var deleteDate = new Date();
                deleteDate.setTime(deleteDate.getTime() - (864000000));
                deleteDate = deleteDate.toGMTString();
                aCookies = document.cookie.split('; ');
                for (i = 0; i < aCookies.length; i++) {
                    aCookie = aCookies[i].split('=');
                    if (aCookie[0].indexOf('_') >= 0) {
                        document.cookie = aCookie[0] + '=0; expires=' + deleteDate + '; domain=' + options.domain.replace('www', '') + '; path=/';
                    } else {
                        document.cookie = aCookie[0] + '=0; expires=' + deleteDate + '; path=/';
                    }
                }
                document.cookie = cookieEntry.replace('{value}', 'declined');
                removeBar(options.declineFunction);
            };
            var anyClick = function (e) {
                if (!$(e.target).hasClass('cb-policy')) cookieAccept();
            };

            $('#cookie-bar .cb-enable').click(function () {
                cookieAccept();
                return false;
            });
            $('#cookie-bar .cb-disable').click(function () {
                cookieDecline();
                return false;
            });
            if (options.acceptOnScroll) {
                var scrollStart = $(document).scrollTop(), scrollNew, scrollDiff;
                $(document).on('scroll', function () {
                    scrollNew = $(document).scrollTop();
                    if (scrollNew > scrollStart) {
                        scrollDiff = scrollNew - scrollStart;
                    } else {
                        scrollDiff = scrollStart - scrollNew;
                    }
                    if (scrollDiff >= Math.round(options.acceptOnScroll)) cookieAccept();
                });
            }
            if (options.acceptAnyClick) {
                $(document).bind('click', anyClick);
            }
        }
    };
})(jQuery);

function policyshow() {
	$('body').prepend('<div id="policy" class="fixed"><p>healthsites.io cannot guarantee the validity of the information found here <a href="https://github.com/healthsites/healthsites/wiki/Healthsites---terms-of-use" target="_blank">Terms of use</a> <a href="#" class="accept">Accept</a></p></div>');
	$('body').addClass('policy-enabled');
	$('.accept').click(function() {
		$('#policy').slideUp(300);
		$('body').removeClass('policy-enabled');
	});
	return false;
}

function renderCredit() {
    /* map credits */
    $("#map").append("<a class='credits' href='#'>&copy;</a>");
    $(".credits").click(function () {
        $(this).hide();
        $(".leaflet-bottom.leaflet-right").show();
        $(".leaflet-bottom.leaflet-right").prepend("<a class='close' href='#'>x</a>");
        return false;
    });
    $(".leaflet-bottom").delegate('.close', 'click', function () {
        $(this).hide();
        $(".leaflet-bottom.leaflet-right").hide();
        $(".credits").show();
        return false;
    });
}

function changePage(element) {
    var childs = $("#updates-wrapper").children();
    var activeChild = $("#updates-wrapper").children(".graph.updates:visible");
    var activeindex = $(activeChild).attr('id').split("-")[1];
    var newActiveIndex = parseInt(activeindex);
    if ($(element).hasClass("prev")) {
        if (activeindex > 0) {
            newActiveIndex -= 1;
        }
    } else if ($(element).hasClass("next")) {
        if (activeindex + 1 < childs.length) {
            newActiveIndex += 1;
        }
    }
    $(activeChild).hide();
    $("#updates-" + newActiveIndex).show();
    updateButton();
    return false;
}

function updateButton() {
    var childs = $("#updates-wrapper").children();
    var activeChild = $("#updates-wrapper").children(".graph.updates:visible");
    var activeindex = $(activeChild).attr('id').split("-")[1];
    $(".prev").removeClass("opacity-7");
    $(".next").removeClass("opacity-7");
    if (activeindex == 0) {
        $(".prev").addClass("opacity-7");
    }
    if (activeindex + 1 >= childs.length) {
        $(".next").addClass("opacity-7");
    }
}