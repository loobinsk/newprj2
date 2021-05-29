$(function () {

  $('.catalog__wrap').click(function (e) {
        var containerWidth = $('body').find('.menu__shift').outerWidth();
        if ((containerWidth < 1230) && (e.target.tagName != 'IMG')) {
            var good_url = $(this).data('url');
            location.href = good_url;
        }
    });


  var icon_cart = $('.icon-cart-good');
  icon_cart.click(function () {
    $(this).closest('.cart-form').submit();
    $(this).parent().find('.cart-popover').text('Товар в корзине')
  });

  $(document).on("click", '.cart-add-btn.btn_orange', function(event) {
    $(this).closest('.cart-form').submit();
    $(this).removeClass('btn_orange');
    $(this).addClass('btn_violet');
    $(this).text('Перейти в корзину');
  });

  $(document).on("click", '.cart-add-btn.btn_violet', function(event) {
    window.location = '/shop/cart/'
  });

  $('body').find('.cart-add-btn').click(function () {
    console.log('!!!');
  });

  icon_cart.mouseenter(function () {
    $(this).parent().find('.cart-popover').removeClass('hidden')
  });
  icon_cart.mouseleave(function () {
    $(this).parent().find('.cart-popover').addClass('hidden')
  })
});