define([
    'backbone',
    'jquery',
], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/schema/',
        el: '#filter-dashboard',
        events: {
            'click .cancel-btn': 'resetFilter',
            'click .apply-btn': 'applyFilter',
        },
        contentWrapper: '#filter-content',
        allowedFilters: [
            'amenity', 'healthcare', 'speciality', 'health_amenity_type', 'operational_status', 'electricity',
            'emergency', 'dispensing'],
        initialize: function (activate) {
            let that = this;
            $('#filter-tab').click(function () {
                that.toggleFilter()
            })
            if (activate) {
                this.getData();
            } else {
                $('.filter-button-wrapper').hide();
            }
        },
        /** Getting data filter from schema
         */
        getData: function () {
            let that = this;
            $.ajax({
                url: this.url,
                success: function (data) {
                    let _data = data['facilities']['create']['fields'];
                    for (let i = 0; i < _data.length; i++) {
                        if (_data[i]['key'] === 'tag') {
                            that.renderForm(_data[i]['tags'])
                        }
                    }
                },
                error: function (err) {
                    console.log(err)
                }
            })
        },
        /** Rendering for for tags data
         * @param data
         */
        renderForm: function (data) {
            const that = this;
            let $wrapper = $(this.contentWrapper);
            $.each(data, function (index, value) {
                if (!that.allowedFilters.includes(value["key"])) {
                    return
                }

                // override the label
                const label = value['key'] === 'health_amenity_type' ? 'Equipment' : value['key'];
                if (value.hasOwnProperty('options')) {
                    let $wrapperItem = $(`<div class="filter-item" data-key="${value["key"]}"></div>`);
                    $wrapperItem.append(`<label class="label-options" for="${value["key"]}">${humanize(label)}</label>`);
                    let $optionWrapper = $('<div class="option-item-wrapper"></div>');
                    for (let j = 0; j < value['options'].length; j++) {
                        $optionWrapper.append(`
                            <div class="option-item">
                                <input type="checkbox" value="${value["options"][j]}" id="${value["key"]}-${value["options"][j]}">
                                <label for="${value["key"]}-${value["options"][j]}">${humanize(value["options"][j])}</label>
                            </div>`)
                    }
                    $wrapperItem.append($optionWrapper);
                    $wrapper.append($wrapperItem)
                } else if (value['type'] === 'boolean') {
                    $wrapper.append(`
                        <div class="filter-item" data-key="${value["key"]}">
                            <label for="${value["key"]}">${humanize(value["key"])}</label>
                            <select class="form-control" type="text" id="${value["key"]}">
                                <option></option>
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>`
                    )
                } else {
                    $wrapper.append(`
                        <div class="filter-item" data-key="${value["key"]}">
                            <label for="${value["key"]}">${humanize(value["key"])}</label>
                            <input class="form-control" type="text" id="${value["key"]}">
                        </div>`
                    )
                }
            });
        },
        /** Toggle filters */
        toggleFilter: function () {
            let $wrapper = $('#filter-dashboard');
            if (!$wrapper.hasClass('active')) {
                $wrapper.show();
                $wrapper.addClass('active');
                $('#filter-tab').css('right', '274px')
            } else {
                $wrapper.hide();
                $wrapper.removeClass('active');
                $('#filter-tab').css('right', '-26px')
            }

        },
        /** Apply filter **/
        applyFilter: function () {
            // $(this.el).find('button').prop('disabled', true);
            let data = {}
            $('#filter-tab').removeClass('active')
            $('.filter-item').each(function (index) {
                let values = []
                $(this).find('input:checked').each(function (index) {
                    values.push($(this).attr('value'));
                });
                $(this).find('select').each(function (index) {
                    if ($(this).val()) {
                        values.push($(this).val());
                    }
                });

                if (values.length > 0) {
                    console.log(values)
                    data[$(this).data('key')] = values
                    $('#filter-tab').addClass('active')
                }
            });
            dataFilters = data;
            shared.dispatcher.trigger('cluster.reload');
            shared.dispatcher.trigger('statistic.rerender');
        },
        /** reset filter **/
        resetFilter: function () {
            $('input[type=checkbox]').each(function () {
                $(this).prop('checked', false)
            });
            $('input[type=text]').each(function () {
                $(this).val('')
            })
            this.applyFilter();
        }
    })
});