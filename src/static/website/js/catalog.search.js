$(document).ready(function() {

    $('.brand-select').change(function () {
        $.ajax({
            url: '/shop/ajax/brand/' + $(this).val() +'/',
            type: 'GET',
            cache: false
        }).done(function(data) {
            $('.good-select').html(data);
            create_custom_dropdowns();
            set_model_select();
        });
    });

});

function set_model_select() {

    $('.good-select select').change(function () {
        window.location.href = $(this).val();
    });

}