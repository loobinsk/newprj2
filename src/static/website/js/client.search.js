$(function() {

    $('.header__search .input').keyup(function () {
        var elem = $(this);
        var q = $(this).val();
        if (q.length < 2) {
            $('#search_content').hide();
        } else {
            $.get("/shop/ajax/search/?q=" + $(this).val(), function (data) {
                elem.parent().find('.search_content').show();
                elem.parent().find('.search_content').html(data);
            });
        }
    });

});