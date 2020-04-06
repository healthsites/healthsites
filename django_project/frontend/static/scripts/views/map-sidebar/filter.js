define([
    'backbone',
    'jquery',
], function (Backbone, $) {
    return Backbone.View.extend({
        url: '/api/schema/',
        contentWrapper: '#filter-content',
        initialize: function () {
            let that = this;
            this.getData();
            $('#filter-tab').click(function () {
                that.toggleFilter()
            })
        },
        getData: function () {
            let that = this;
            $.ajax({
                url: this.url,
                success: function (data) {
                    let _data = data['facilities']['create']['fields'];
                    for(let i=0; i<_data.length; i++){
                        if(_data[i]['key'] === 'tag'){
                            that.renderForm(_data[i]['tags'])
                        }}
                },
                error: function (err) {
                    console.log(err)
                }
            })
        },
        renderForm: function (data) {
            let that = this;
            let $wrapper = $(this.contentWrapper);
            $wrapper.html('');
            for(let i=0; i<data.length; i++){
                if(data[i].hasOwnProperty('options')){
                    let $wrapperItem = $('<div class="filter-item"></div>');
                    $wrapperItem.append('<label class="label-options" for="' + data[i]["key"] + '">' + data[i]["key"] + '</label>');
                    let $optionWrapper = $('<div class="option-item-wrapper"></div>');
                    for(let j=0; j<data[i]['options'].length; j++){
                        $optionWrapper.append('<div class="option-item">' +
                            '<input type="checkbox" value="' + data[i]["options"][j] + '" id="' + data[i]["key"] + "-" + data[i]["options"][j] + '">' +
                            '<label for="' + data[i]["key"] + "-" + data[i]["options"][j] + '"> ' + data[i]["options"][j] + '</label>' +
                            '</div>')
                    }
                    $wrapperItem.append($optionWrapper);
                    $wrapper.append($wrapperItem)
                }else {
                    $wrapper.append('' +
                        '<div class="filter-item">' +
                        '<label for="' + data[i]["key"] + '">' + data[i]["key"] + '</label>' +
                        '<input class="form-control" type="text" id="' + data[i]["key"] + '">' +
                        '</div>'
                    )
                }
            }
            $wrapper.append('' +
                '<button class="btn btn-primary">Apply</button>' +
                '<button class="cancel-btn btn btn-danger">Reset</button>'
            );
            $('.cancel-btn').click(function () {
                that.resetFilter();
            })
        },
        toggleFilter: function () {
            let $wrapper = $('#filter-dashboard');
            if(!$wrapper.hasClass('active')){
                $wrapper.show();
                $wrapper.addClass('active');
                $('#filter-tab').css('right', '274px')
            } else {
                $wrapper.hide();
                $wrapper.removeClass('active');
                $('#filter-tab').css('right', '-26px')
            }

        },
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