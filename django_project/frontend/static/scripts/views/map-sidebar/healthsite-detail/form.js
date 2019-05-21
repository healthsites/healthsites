define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        definitions: {
            name: {
                required: true,
                type: 'string',
                description: 'name of healthsites',
            },
            amenity: {
                required: true,
                type: 'selection',
                description: 'amenity of healthsites',
                options: ['clinic', 'doctors', 'hospital', 'dentist', 'pharmacy']
            }
        },
        initialize: function () {
            this.renderInitForm();
        },
        renderInitForm: function () {
            $.each(this.definitions, function (tag, value) {
                var inputHtml = '';
                switch (value['type']) {
                    case 'string':
                        inputHtml = '<input class="input" type="text" placeholder="' + value['description'] + '">';
                        break;
                    case 'selection':
                        inputHtml = "<select class='input'>";
                        var options = value['options'];
                        $.each(options, function (index, key) {
                            inputHtml += '<option value="' + key + '">' + key + '</option>';
                        });
                        inputHtml += "</select>";
                        break;
                }
                var $element = $('*[data-tag="' + tag + '"]');
                if ($element.length > 0) {
                    $element.append(inputHtml);
                }
            })
        }
    })
});

