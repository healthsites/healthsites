define([
    'backbone',
    'jquery',
], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/schema/',
        el: '#filter-dashboard',
        events: {
            'click .cancel-btn': 'resetFilter'
        },
        contentWrapper: '#filter-content',
        allowedFilters: ['amenity', 'healthcare'],
        initialize: function () {
            let that = this;
            this.getData();
            $('#filter-tab').click(function () {
                that.toggleFilter()
            })
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
                if (value.hasOwnProperty('options')) {
                    let $wrapperItem = $(`<div class="filter-item" data-key="${value["key"]}"></div>`);
                    $wrapperItem.append(`<label class="label-options" for="${value["key"]}">${value["key"]}</label>`);
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
                } else {
                    $wrapper.append(`
                        <div class="filter-item" data-key="${value["key"]}">
                            <label for="${value["key"]}">${value["key"]}</label>
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
        /** reset filter **/
        resetFilter: function () {
            $('input[type=checkbox]').each(function () {
                $(this).prop('checked', false)
            });
            $('input[type=text]').each(function () {
                $(this).val('')
            })
        }
    })
});