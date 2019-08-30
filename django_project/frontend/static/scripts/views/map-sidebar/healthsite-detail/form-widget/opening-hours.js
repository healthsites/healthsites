define([
    'backbone',
    'jquery',
    'timePicker'], function (Backbone, $, timePicker) {
    return Backbone.View.extend({
        selectedClass: 'selected',
        timeRegex: /([01][0-9]|[02][0-3]):[0-5][0-9]/,
        initialize: function () {
            var self = this;
            this.$el = $('#op-hr');
            this.$el.find('.btn-group button').click(function () {
                self.toggleButton($(this));
            });
            this.$el.find('.fa-plus-square').each(function (index) {
                $(this).click(function () {
                    self.addNewTime($(this).closest('tr').find('.op-hr-input'), true);
                });
            });
            this.toDefault();
        },
        toDefault: function () {
            var self = this;
            // create default time
            $(".op-hr-input").each(function (index) {
                $(this).html('');
                self.addNewTime($(this));
            });
            $(this.$el.find('.btn-group button')[0]).click();
        },
        toggleButton: function ($element) {
            this.$el.find('.btn-group button').removeClass(this.selectedClass);
            $('.op-hr-section').hide();
            $element.addClass(this.selectedClass);
            $('#op-hr-' + $element.data('target')).show();

            // rerender time width
            this.$el.find('#op-hr-section-wrapper').width(this.$el.find('.btn-group').width());
        },
        addNewTime: function ($wrapper, ableRemove) {
            var self = this;
            var $template = $($('#_op-hr-timepicker').html());
            $wrapper.append($template);

            // check remove button
            var $minusButton = $template.find('.fa-minus-square');
            if (!ableRemove) {
                $minusButton.hide();
            } else {
                $minusButton.click(function () {
                    // setup prev and next timepicker
                    let $currentTime = $template.find('.time-from');
                    let $timepickers = $wrapper.find('.timepicker');
                    let currentIndex = $timepickers.index($currentTime);
                    let $prevTime = $timepickers.eq(currentIndex - 1);
                    $template.remove();
                    self.setupCurrentTimePicker(
                        $wrapper, $prevTime);
                });
            }

            // init timepicker
            $template.find('.timepicker').timepicker({
                timeFormat: 'H:i',
                interval: 15
            });
            $template.find('.timepicker').change(function () {
                if (!self.checkTimeFormat($(this).val())) {
                    $(this).val($(this).attr('value'));
                } else {
                    self.setupOtherTimePicker($wrapper, $(this));
                    $(this).attr('value', $(this).val());
                }
            });
            this.setupCurrentTimePicker($wrapper, $template.find('.time-from'));

        },
        setupOtherTimePicker: function ($wrapper, $element) {
            // Set up min max time when a timepicker changed
            let $currentTime = $element;
            let $timepickers = $wrapper.find('.timepicker');
            let currentIndex = $timepickers.index($currentTime);

            // setup prev and next timepicker
            if (currentIndex > 0) {
                let $prevTime = $timepickers.eq(currentIndex - 1);
                this.setupCurrentTimePicker($wrapper, $prevTime);
            }
            if (currentIndex + 1 < $timepickers.length) {
                let $nextTime = $timepickers.eq(currentIndex + 1);
                this.setupCurrentTimePicker($wrapper, $nextTime);
            }
        },
        setupCurrentTimePicker: function ($wrapper, $element) {
            // Set up min max time when a timepicker changed
            let $currentTime = $element;
            let $timepickers = $wrapper.find('.timepicker');
            let currentIndex = $timepickers.index($currentTime);

            // setup prev and next timepicker
            if (currentIndex > 0) {
                let $prevTime = $timepickers.eq(currentIndex - 1);
                $currentTime.timepicker(
                    'option',
                    {'minTime': $prevTime.val()});
                if ($currentTime.val() < $prevTime.val()) {
                    $currentTime.val($prevTime.val());
                }
            }
            if (currentIndex + 1 < $timepickers.length) {
                let $nextTime = $timepickers.eq(currentIndex + 1);
                $currentTime.timepicker(
                    'option',
                    {'maxTime': $nextTime.val()});
                if ($currentTime.val() > $nextTime.val()) {
                    $currentTime.val($nextTime.val());
                }
            } else {
                $currentTime.timepicker(
                    'option',
                    {'maxTime': '23:55'});
            }
        },
        checkTimeFormat: function (time) {
            if (time.length !== 5) {
                return false;
            }
            return time.search(this.timeRegex) >= 0;
        },
        getDefiningHoursPerSection: function ($element) {
            var hours = [];
            $element.find('.op-hr-input div').each(function () {
                var timeFrom = $(this).find('.time-from').val();
                var timeTo = $(this).find('.time-to').val();
                hours.push(timeFrom + '-' + timeTo);
            });
            return '' + hours;
        },
        getDefiningHours: function () {
            var self = this;
            var output = null;
            var timeType = this.$el.find('.btn-group button.selected').data('target');
            if (timeType === 'all-time') {
                output = '24/7';
            } else if (timeType === 'weekday') {
                output = 'Mo-Fr ' + this.getDefiningHoursPerSection($('#op-hr-weekday'));
            } else if (timeType === 'weekend') {
                output = 'Sa-Su ' + this.getDefiningHoursPerSection($('#op-hr-weekend'));
            } else if (timeType === 'custom') {
                var days = [];
                $('#op-hr-custom tr').each(function () {
                    if (!$(this).find('input[type="checkbox"]').is(":checked")) {
                        days.push({
                            'day-from': $(this).data('day')
                        })
                    } else {
                        var time = self.getDefiningHoursPerSection($(this));
                        var currentDayTime = days[days.length - 1];
                        if (currentDayTime && currentDayTime['time'] === time) {
                            currentDayTime['day-to'] = $(this).data('day');
                        } else {
                            days.push({
                                'day-from': $(this).data('day'),
                                'time': time
                            })
                        }
                    }
                });

                let cleanTimes = [];
                $.each(days, function (index, value) {
                    if (value['time']) {
                        let cleanDayTime = value['day-from'];
                        if (value['day-to']) {
                            cleanDayTime += '-' + value['day-to']
                        }
                        cleanDayTime += ' ' + value['time'];
                        cleanTimes.push(cleanDayTime);
                    }
                });
                output = cleanTimes.join('; ');
            }
            return output;
        },
    })
});

