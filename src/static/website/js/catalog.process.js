$(document).ready(function () {

  set_good_js();

});


function set_good_js() {

  $("[data-fancybox]").fancybox({
       afterClose : function(){$('.magnifier, .cursorshade, .statusdiv, .tracker').remove();},
    afterShow: function (instance, slide) {

      $('.card').click(function (e) {

        var elem = $(e.target);
        if (elem.hasClass('link') || elem.hasClass('btn') || elem.hasClass('slick-slide')) {
          return;

        }
        if (elem.hasClass('fancybox-close-small')) {
          return;
        }

        if (elem.is( "img" )) {
          return;
        }

        location.href = $(this).attr('data-url');
      });

      var $slickSlide = $('body').find('.card__good__slide');
      var slickSlideSettings = {
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.card__good__nav',
      }
      var $slickNav = $('body').find('.card__good__nav');
      var slickNavSettings = {
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.card__good__slide',
        vertical: true,
        centerMode: false,
        focusOnSelect: true,
        prevArrow: '<svg class="icon icon-arrowTop"><use xlink:href="#arrowTop"></use></svg>',
        nextArrow: '<svg class="icon icon-arrowBottom"><use xlink:href="#arrowBottom"></use></svg>',
        responsive: [{
          breakpoint: 1230,
          settings: {
            vertical: false,
            prevArrow: '<svg class="icon icon-arrowLeft"><use xlink:href="#arrowLeft"></use></svg>',
            nextArrow: '<svg class="icon icon-arrowRight"><use xlink:href="#arrowRight"></use></svg>',
          }
        }]
      }

      $('.card__good__nav, .card__good__slide').show();
      $slickSlide.slick(slickSlideSettings)
        .on('afterChange', function () {
          $('.slick-active .zoom').imagezoomsl({
            zoomrange: [3, 3],
            magnifiersize: [411, 531],
            cursorshadeborder: '1px solid #c0c0c0',
            rightoffset: 80
          })
        })
        .on('beforeChange', function () {
          $('.magnifier, .cursorshade, .statusdiv, .tracker').remove();
        });
      $slickNav.slick(slickNavSettings)
      $('.slick-active .zoom').imagezoomsl({
        zoomrange: [3, 3],
        magnifiersize: [411, 531],
        cursorshadeborder: '1px solid #c0c0c0',
        rightoffset: 80
      });

      $('.slick-active').mouseover(function () {
        $(this).click();
      });


      var params = $('.catalog__fast__links .card__param').find('.toggle__click');
      var dev = $('.catalog__fast__links .card__dev').find('.toggle__click');
      params.click(function () {
        $(this).toggleClass('link_actvie')
          .next('.toggle__content').toggle();
        dev.removeClass('link_actvie')
          .next('.toggle__content').hide();

      })
      dev.click(function () {
        $(this).toggleClass('link_actvie')
          .next('.toggle__content').toggle();
        params.removeClass('link_actvie')
          .next('.toggle__content').hide();

      })


    }


  });


   var slickSlides = $('body').find('.cat__good__slide');

  $('body').find('.cat__good__slide').each(function(index) {
    var slide = $(this);
    var nav_id = slide.data('nav-id');
    var slide_id = slide.attr('id');
    var slickSlideSettings = {
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      fade: true,
      asNavFor: '#' + nav_id,
    }
    var slickNavSettings = {
      slidesToShow: 4,
      slidesToScroll: 1,
      asNavFor: '#' + slide_id,
      vertical: true,
      centerMode: false,
      focusOnSelect: true,
      prevArrow: '<svg class="icon icon-arrowTop"><use xlink:href="#arrowTop"></use></svg>',
      nextArrow: '<svg class="icon icon-arrowBottom"><use xlink:href="#arrowBottom"></use></svg>',
      responsive: [{
        breakpoint: 1230,
        settings: {
          vertical: false,
          prevArrow: '<svg class="icon icon-arrowLeft"><use xlink:href="#arrowLeft"></use></svg>',
          nextArrow: '<svg class="icon icon-arrowRight"><use xlink:href="#arrowRight"></use></svg>',
        }
      }]
    }

    slide.slick(slickSlideSettings);
    $('#' + nav_id).slick(slickNavSettings);
  });

  $(document).on('mouseover', '.slick-active', function () {
    $(this).click();
  });

}