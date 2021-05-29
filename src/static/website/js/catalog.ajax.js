$(document).ready(function() {

    catalog_init();

    $('#catalog_sort_tablet').next().find('.option').click(function (e) {
        var sort_val = $(this).data('value').split('_');
        SHOP_SORT_FIELD = sort_val[0];
        SHOP_SORT_DIRECTION = sort_val[1];
        catalog_show();
    });

    $('.brand_page_input').click(function () {
        $('.brand_page_input:checked').prop('checked', false);
        $(this).prop('checked', true);
        var brand_url = $(this).attr('data-url');
        show_loading();
        location.href = brand_url;
    });


    $('.catalog_sort_name_link').click(function () {

        if (SHOP_SORT_FIELD == 'name' && SHOP_SORT_DIRECTION == 'asc') {
            SHOP_SORT_DIRECTION = 'desc';
        } else {
            SHOP_SORT_DIRECTION = 'asc';
        }
        SHOP_SORT_FIELD = 'name';
        catalog_show();
    });

    $('.catalog_sort_price_link').click(function () {

        if (SHOP_SORT_FIELD == 'price' && SHOP_SORT_DIRECTION == 'asc') {
            SHOP_SORT_DIRECTION = 'desc';
        } else {
            SHOP_SORT_DIRECTION = 'asc';
        }
        SHOP_SORT_FIELD = 'price';
        catalog_show();
    });

    $('.catalog_show_count_li').click(function (e) {
        e.preventDefault();
        SHOP_SHOW_COUNT = $(this).text();
        SHOP_PAGE = 1;
        catalog_show();
    });

    $('.catalog_avail').change(function () {
        SHOP_PAGE = 1;
        catalog_show();
        show_filters();
        show_brands();
    });

    $('.catalog_actual').change(function () {
        SHOP_PAGE = 1;
        catalog_show();
        show_filters();
        show_brands();
    });

    $('.catalog-filter__reset_nf').click(function () {
        SHOP_PAGE = 1;
        catalog_show();
        show_filters();
        show_brands();
    });

    set_filters_js();
    set_filters_brands_js();
    set_categories_js();
    set_prices_js();

});

function catalog_show() {

    catalog_init();
    show_loading();

    var avail = [];
    $('.catalog_avail').each(function () {
        if ($(this).prop('checked')) {
            avail.push($(this).val());
        }
    });

    var actual = [];
    $('.catalog_actual').each(function () {
        if ($(this).prop('checked')) {
            actual.push($(this).val());
        }
    });

    var data = {
        'sort_direction': SHOP_SORT_DIRECTION, 'sort_field': SHOP_SORT_FIELD, 'category': SHOP_CATEGORY,
        'brand': SHOP_BRAND, 'is_new': SHOP_IS_NEW, 'is_sale': SHOP_IS_SALE, 'show_count': SHOP_SHOW_COUNT,
        'page': SHOP_PAGE, 'avail': avail, 'actual': actual, 'q': SHOP_SEARCH_Q, 'properties': SHOP_PROPERTIES,
        'brands': SHOP_BRANDS, 'price': SHOP_PRICE, 'categories': SHOP_CATEGORIES
    };

    $.ajax({
        url: SHOP_AJAX_URL,
        type: 'GET',
        cache: false,
        data: data
    }).done(function(data) {
        $('.ajax-goods').html(data);
        SHOP_PAGE_COUNT = parseInt($('#catalog-page-count').text());
        $('.shop_count').html($('#catalog-count').html());
        set_good_js();
        catalog_init();
        //alert('1111');
    }).always(function() {
        hide_loading();
    });

}


function catalog_init() {

    var elem;

    $('.catalog_sort_link svg').hide();
    elem = $('.catalog_sort_' + SHOP_SORT_FIELD + '_link svg');
    elem.show();

    if (SHOP_SORT_DIRECTION == 'asc') {
        elem.addClass('sort_up');
    } else {
        elem.removeClass('sort_up');
    }

    $('.catalog_show_count_li a').removeClass('active');
    $('.catalog_show_count_li_'+ SHOP_SHOW_COUNT + ' a').addClass('active');

    if (SHOP_PAGE_COUNT <= 1) {
        $('.pagination__page').hide();
    } else {
        $('.pagination__page').show();
    }

    show_paging();

}

function show_paging() {

    var paging_count = 2;


    var first = '<li class="pagination__prev"><a href="" class="link pagination__item__prev"><svg class="icon icon-arrowLineH"><use xlink:href="#arrowLineH"></use></svg> </a> </li>';
    var last = '&nbsp;&nbsp;&nbsp;<li class="pagination__next"><a href="" class="link pagination__item__next"><svg class="icon icon-arrowLineH"><use xlink:href="#arrowLineH"></use></svg></a></li>';
    var first_m = '<li class="pagination__nav pagination__item__prev"><svg class="icon icon-pagLeft"><use xlink:href="#pagLeft"></use></svg></li>';
    var last_m = '<li class="pagination__nav pagination__item__next"><svg class="icon icon-pagRight"><use xlink:href="#pagRight"></use></svg></li>';


    var p_body = '';
    var m_body = '';
    var prev = 1;

    for (var i = 1; i <= SHOP_PAGE_COUNT; i++) {

        if ((i <= SHOP_PAGE + paging_count && i >= SHOP_PAGE - paging_count) || (i <= paging_count) || (i > SHOP_PAGE_COUNT - paging_count)){
            if (prev < i - 1) {
                var s = '<li class="pagination__item">...</li>';
                p_body += s;
                var s = '<li>...</li>';
                m_body += s;
            }
            prev = i;
            if (SHOP_PAGE == i) {
                var s = '<li class="pagination__item pagination__item__page"><a href="" class="active">' + i + '</a></li>';
                var sm = '<li class="active pagination__item__page">' + i + '</li>';
            } else {
                var s = '<li class="pagination__item pagination__item__page"><a href="" class="link">' + i + '</a></li>';
                var sm = '<li class="pagination__item__page">' + i + '</li>';
            }
            p_body += s;
            m_body += sm;
        }
    }

    $('.pagination-js').html(first + p_body + last);
    $('.pagination-js-m').html(first_m + m_body + last_m);
    init_js();
}

function show_loading() {
    $('<div class="fancybox-container fancybox-is-open" role="dialog" tabindex="-1" id="fancybox-container-1" style="transition-duration: 366ms;"><div class="fancybox-bg"></div><div class="fancybox-inner"><div class="fancybox-stage"><div class="fancybox-slide fancybox-slide--current fancybox-slide--ajax" style=""><div class="fancybox-loading"></div></div></div><div class="fancybox-caption-wrap"><div class="fancybox-caption"></div></div></div></div>').prependTo('.ajax-goods').css({});
}

function hide_loading() {
    $('.fancybox-container').remove();
}

function init_js() {

    $('.pagination__item__page').click(function (e) {
        e.preventDefault();
        SHOP_PAGE = parseInt($(this).text());
        catalog_show();
    });

    $('.pagination__item__prev').click(function (e) {
        e.preventDefault();
        if (SHOP_PAGE > 1) {
            SHOP_PAGE += -1;
            catalog_show();
        }
    });

    $('.pagination__item__next').click(function (e) {
        e.preventDefault();
        if (SHOP_PAGE < SHOP_PAGE_COUNT) {
            SHOP_PAGE += 1;
            catalog_show();
        }
    });

}

function calc_properties() {
    SHOP_PROPERTIES = [];
    $('.property_input:checked').each(function () {
        if ($(this).prop('checked')) {
            SHOP_PROPERTIES.push($(this).attr('data-id') + '|' + $(this).attr('data-value'));
        }
    });
    SHOP_CATEGORIES = [];
    $('.category_1_input:checked').each(function () {
        if ($(this).prop('checked')) {
            SHOP_CATEGORIES.push($(this).attr('data-id'));
        }
    });
    $('.category_2_input:checked').each(function () {
        if ($(this).prop('checked')) {
            SHOP_CATEGORIES.push($(this).attr('data-id'));
        }
    });
    $('.category_3_input:checked').each(function () {
        if ($(this).prop('checked')) {
            SHOP_CATEGORIES.push($(this).attr('data-id'));
        }
    });
}


function calc_brands() {
    SHOP_BRANDS = [];
    $('.brand_input:checked').each(function () {
        if ($(this).prop('checked')) {
            SHOP_BRANDS.push($(this).attr('data-id'));
        }
    });
}

function show_brands() {

    var avail = [];
    $('.catalog_avail').each(function () {
        if ($(this).prop('checked')) {
            avail.push($(this).val());
        }
    });

    var actual = [];
    $('.catalog_actual').each(function () {
        if ($(this).prop('checked')) {
            actual.push($(this).val());
        }
    });

    $.ajax({
        url: shop_url_filters_brands,
        type: 'GET',
        cache: false,
        data: {'category': SHOP_CATEGORY, 'brand': SHOP_BRAND, 'properties': SHOP_PROPERTIES, 'is_new': SHOP_IS_NEW,
            'is_sale': SHOP_IS_SALE, 'avail': avail, 'actual': actual, 'brands': SHOP_BRANDS, 'price': SHOP_PRICE,
            'categories': SHOP_CATEGORIES}
    }).done(function(data) {
        $('#filters_brands').html(data);
        set_filters_brands_js();
        //alert('22222');
    });

}


function show_filters() {

    var avail = [];
    $('.catalog_avail').each(function () {
        if ($(this).prop('checked')) {
            avail.push($(this).val());
        }
    });

    var actual = [];
    $('.catalog_actual').each(function () {
        if ($(this).prop('checked')) {
            actual.push($(this).val());
        }
    });

    if($('#filters_categories').length ) {
        $.ajax({
            url: shop_url_filters_categories,
            type: 'GET',
            cache: false,
            data: {'category': SHOP_CATEGORY, 'brand': SHOP_BRAND, 'properties': SHOP_PROPERTIES, 'is_new': SHOP_IS_NEW,
                'is_sale': SHOP_IS_SALE, 'avail': avail, 'actual': actual, 'brands': SHOP_BRANDS, 'price': SHOP_PRICE,
                'categories': SHOP_CATEGORIES}
        }).done(function(data) {
            $('#filters_categories').html(data);
            set_categories_js();
            //alert('1111');
        });
    }

    $.ajax({
        url: shop_url_filters,
        type: 'GET',
        cache: false,
        data: {'category': SHOP_CATEGORY, 'brand': SHOP_BRAND, 'properties': SHOP_PROPERTIES, 'is_new': SHOP_IS_NEW,
            'is_sale': SHOP_IS_SALE, 'avail': avail, 'actual': actual, 'brands': SHOP_BRANDS, 'price': SHOP_PRICE,
            'categories': SHOP_CATEGORIES}
    }).done(function(data) {
        $('#filters').html(data);
        set_filters_js();
        //alert('1111');
    });


}


function set_categories_js() {

  $('.catalog-filter__reset_c').click(function () {
        SHOP_PAGE = 1;
        $(this).parent().next().find('input:checkbox').each(function () {
            $(this).prop('checked', false);
        });
        SHOP_PRICE = null;
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
        show_prices();
    });


    $('.category_1_input').click(function () {
        var checked = $(this).prop('checked');
        $('.category_1_input:checked').prop('checked', false);
        $('.category_2_input:checked').prop('checked', false);
        $('.category_3_input:checked').prop('checked', false);
        $(this).prop('checked', checked);
        SHOP_PAGE = 1;
        SHOP_PRICE = null;
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
        show_props();
        show_prices();
    });

    $('.category_2_input').click(function () {
        var checked = $(this).prop('checked');
        $('.category_2_input:checked').prop('checked', false);
        $('.category_3_input:checked').prop('checked', false);
        $(this).prop('checked', checked);
        SHOP_PAGE = 1;
        SHOP_PRICE = null;
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
        show_props();
        show_prices();
    });

    $('.category_3_input').click(function () {
        var checked = $(this).prop('checked');
        $('.category_3_input:checked').prop('checked', false);
        $(this).prop('checked', checked);
        SHOP_PAGE = 1;
        SHOP_PRICE = null;
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
        show_props();
        show_prices();
    });

  $('.clear-checked_c').each(function() {
    var resetCheck = $(this).prev().find('.reset-checked'),
        checkBox = $(this).find('input:checkbox');

      if($(checkBox).is(':checked'))
        resetCheck.show();
      $(checkBox).change(function() {
        if(!$(checkBox).is(':checked'))
          resetCheck.hide();
        else
          resetCheck.show();
      })
  });

  // slideUp / Down catalog group elements
  $('.dropdown__toggle_c').click(function() {
    var $this = $(this).parent().find('.icon').parent(),
        content = $this.parent().next();
    if ( content.is(':hidden') ) {
      content.show('fast');
      $this.removeClass('hide');
    } else {
      content.slideUp('fast');
      $this.addClass('hide');
    }
  });

}


function set_filters_js() {

    $('.catalog-filter__reset_f').click(function () {
        SHOP_PAGE = 1;
        $(this).parent().next().find('input:checkbox').each(function () {
            $(this).prop('checked', false);
        });
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
    });

    $('.property_input').click(function () {
        SHOP_PAGE = 1;
        calc_properties();
        catalog_show();
        show_filters();
        show_brands();
    });

  $('.clear-checked_f').each(function() {
    var resetCheck = $(this).prev().find('.reset-checked'),
        checkBox = $(this).find('input:checkbox');

      if($(checkBox).is(':checked'))
        resetCheck.show();
      $(checkBox).change(function() {
        if(!$(checkBox).is(':checked'))
          resetCheck.hide();
        else
          resetCheck.show();
      })
  });

  // slideUp / Down catalog group elements
  $('.dropdown__toggle_f').click(function() {
    var $this = $(this).parent().find('.icon').parent(),
        content = $this.parent().next();
    if ( content.is(':hidden') ) {
      content.show('fast');
      $this.removeClass('hide');
    } else {
      content.slideUp('fast');
      $this.addClass('hide');
    }
  });

}

function set_filters_brands_js() {

  $('.brand_search').keyup(function () {
      var curr_value = $(this).val();
      $('.clear-checked_b label').each(function () {
          var value = $(this).attr('data-name');
          var idx = value.toLowerCase().search(curr_value.toLowerCase());
          if (idx === -1) {
              $(this).hide();
          } else {
              $(this).show();
          }
      });
  });

  $('.catalog-filter__reset_b').click(function () {
        SHOP_PAGE = 1;
        $(this).parent().next().find('input:checkbox').each(function () {
            $(this).prop('checked', false);
        });
        calc_brands();
        catalog_show();
        show_brands();
        show_filters();
    });

    $('.brand_input').click(function () {
        SHOP_PAGE = 1;
        calc_brands();
        catalog_show();
        show_brands();
        show_filters();
    });

  $('.clear-checked_b').each(function() {
    var resetCheck = $(this).prev().find('.reset-checked'),
        checkBox = $(this).find('input:checkbox');

      if($(checkBox).is(':checked'))
        resetCheck.show();
      $(checkBox).change(function() {
        if(!$(checkBox).is(':checked'))
          resetCheck.hide();
        else
          resetCheck.show();
      })
  });

  // slideUp / Down catalog group elements
  $('.dropdown__toggle_b').click(function() {
    var $this = $(this).parent().find('.icon').parent(),
        content = $this.parent().next();
    if ( content.is(':hidden') ) {
      content.show('fast');
      $this.removeClass('hide');
    } else {
      content.slideUp('fast');
      $this.addClass('hide');
    }
  });

}

function show_props() {

    if ($('.category_1_input:checked').length) {
        $('#filters').show();
    }else {
        $('#filters').hide();
    }
}

function set_prices_js() {

    var resetRange = document.getElementById('resetRange');
    $(resetRange).click(function () {
        SHOP_PAGE = 1;
        SHOP_PRICE = keypressSlider.noUiSlider.get();
        catalog_show();
        show_filters();
        show_brands();
    });

    $('#input-with-keypress-1, #input-with-keypress-0').change(function() {
        SHOP_PAGE = 1;
        SHOP_PRICE = keypressSlider.noUiSlider.get();
        catalog_show();
        show_filters();
        show_brands();
        resetRange.style.display="inline";
    });

    keypressSlider.noUiSlider.on('change', function( values, handle ) {
        SHOP_PAGE = 1;
        SHOP_PRICE = values;
        catalog_show();
        show_filters();
        show_brands();
    });

}

function show_prices() {

    var avail = [];
    $('.catalog_avail').each(function () {
        if ($(this).prop('checked')) {
            avail.push($(this).val());
        }
    });

    var actual = [];
    $('.catalog_actual').each(function () {
        if ($(this).prop('checked')) {
            actual.push($(this).val());
        }
    });

    if($('#filters_prices').length ) {
        $.ajax({
            url: shop_url_filters_prices,
            type: 'GET',
            dataType: 'json',
            cache: false,
            data: {'category': SHOP_CATEGORY, 'brand': SHOP_BRAND, 'is_new': SHOP_IS_NEW, 'is_sale': SHOP_IS_SALE,
                'avail': avail, 'actual': actual, 'brands': SHOP_BRANDS, 'categories': SHOP_CATEGORIES}
        }).done(function(data) {
            var keypressSlider = document.getElementById('keypress');
            SHOP_PRICE = [data.price_min, data.price_max];
            keypressSlider.noUiSlider.updateOptions({
                range: {
                    'min': data.price_min,
                    'max': data.price_max
                }
            });
            keypressSlider.noUiSlider.set(SHOP_PRICE);
        });
    }

}