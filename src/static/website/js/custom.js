$(function () {
    $('#search_button').click(function () {
        var containerWidth = $('body').find('.menu__shift').outerWidth();
        if(containerWidth >= 1230) {
            $('#search-form').submit();
        } else {
            $('#search-overlay').toggle(400);
        }
    });

    $('#menu-panel-close').click(function () {
        $('#menuToggleLevel').click();
    });
    $('#filter-panel-close').click(function () {
        $('#filterToggle').click();
    });
});