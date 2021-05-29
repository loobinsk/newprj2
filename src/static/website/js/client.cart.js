$(function () {
    show_cart_js();
    show_cart_fixbar();
});

function show_cart_js() {

    $('.cart-plus').click(function () {
      var input = $(this).parent().find('input');
      var num =+ input.val()+1;
      input.val(num);
      input.trigger('blur');
    });
    $('.cart-minus').click(function () {
      var input = $(this).parent().find('input');
      var num =+ input.val()-1;
      input.val(num);
      input.trigger('blur');
    });
    $('.cart_count').blur(function (e) {
        var count = $(this).val();
        var available = $(this).attr('max');
        if (parseInt(count) > parseInt(available)) {
            alert('Доступное кол-во для заказа ' + available + ' шт.');
            count = available;
        }
        var id = $(this).attr('data-good');
        $.ajax({
            url: cart_edit_url,
            type: 'GET',
            cache: false,
            data: {'count': count, 'id': id}
        }).done(function() {
            show_cart_fixbar();
            show_cart_content();
        });
        e.preventDefault();
    });

    $('.cart-delete').click(function (e) {
        e.preventDefault();
        var id = $(this).attr('data-good');
        $.ajax({
            url: cart_delete_url,
            type: 'GET',
            cache: false,
            data: {'id': id}
        }).done(function() {
            show_cart_fixbar();
            show_cart_content();
        });
    });

}

function show_cart_content() {

    $.ajax({
        url: cart_url,
        type: 'GET',
        cache: false,
        data: {'back_url': cart_back_url}
    }).done(function(data) {
        $('#cart-content').html(data);
        show_cart_js();
    });

}


function show_cart_add() {

    $(document).on("submit", '.cart-form', function(e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: cart_url_add,
            type: 'GET',
            cache: false,
            data: form.serialize()
        }).always(function() {
            show_cart_fixbar();
            // $('#show_cart_message')[0].click();
        });

    });

}


function show_cart_fixbar() {
    $.ajax({
        url: cart_info_url,
        type: 'GET',
        cache: false
    }).done(function(data) {
        var info = data.split('|');
        $('#fixbar_cart_count').text(info[0]);
        $('#fixbar_cart_sum').text(info[1] + ' руб.');
        $('.cart__count').text(info[0]);
        if (parseInt(info[0]) > 0) {
            $('.cart__count').removeClass('visible-md');
            $('.cart-text').addClass('cart-text-a');
        } else {
            $('.cart__count').addClass('visible-md');
            $('.cart-text').removeClass('cart-text-a');
        }
    });
}