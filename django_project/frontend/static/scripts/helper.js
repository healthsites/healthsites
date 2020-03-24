/** Change select into Select 2 style
 * @param $element
 * @param placeholder = place holder for empty input
 */
function createSelectToSelect2($element, placeholder) {
    try {
        $element.select2('destroy');
    } catch (e) {

    }
    $element.select2({
        placeholder: placeholder,
        allowClear: true
    });
    $('.select2').addClass('input');
}