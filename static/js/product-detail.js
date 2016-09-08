$(function() {
    var rating_ele = $('.seller-rating');

    rating_ele.each(function() {
        var rating = Math.round($(this).attr('data-rating'));
        for(var i=0; i<rating; i++) {
            $($(this).find('i')).each(function(j) {
                if(i == j) {
                    $(this).addClass('active');
                }
            });
        }
    });

    var product_list = $(".product-list");
    var product_list_item = $(".product-list li");
    var product_icon = $('.product-dropdown-icon i');

    $('#product-option, .product-dropdown-icon').on('click', function() {
        if(product_icon.hasClass('fa-caret-down')) {
            product_list.css('display', 'block');
            product_icon.removeClass('fa-caret-down').addClass('fa-caret-up');
        }else {
            product_list.hide();
            product_icon.removeClass('fa-caret-up').addClass('fa-caret-down');
        }
    });

    $(window).click(function(e) {
        if (!product_list_item.is(e.target) && product_list_item.has(e.target).length === 0) {
            if(!$('.product-dropdown').is(e.target) && $('.product-dropdown').has(e.target).length === 0) {
                product_list.hide();
                product_icon.removeClass('fa-caret-up').addClass('fa-caret-down');
            }
        }
    });

    product_list.on('click', 'input[type=checkbox]', function() {
        var count_item = 0;
        var total_price = parseInt($('#product-price').attr('data-price'));
        var product_select = '<div class="product-select-item item-default">' +
                                '기본- <span>' + total_price + '</span>원' +
                             '</div>';

        product_list_item.each(function() {
            if($(this).find('input[type=checkbox]').is(':checked') === true) {
                count_item ++;
                total_price += parseInt($(this).attr('data-price'));
                product_select += '<div class="product-select-item">' +
                                       $(this).attr('data-item') + '- <span>' + $(this).attr('data-price') + '</span>원' +
                                       '<i class="fa fa-times" aria-hidden="true"></i>' +
                                  '</div>';
            }
        });

        $('.product-select-list').html('').html(product_select);
        $('#product-total').text(total_price).digits();
        $('.product-select-item span').digits();

        if(count_item === 0) {
            $('.product-select-item').removeClass('item-default').digits();
        }
    });

    $('.product-select-list').on('click', 'i', function() {
        var delete_item = $(this).parent().text().split('-')[0];

        product_list_item.each(function() {
            if($(this).find('label').text() == delete_item) {
                $(this).find('input[type=checkbox]').trigger('click');
            }
        });
    });

    $('#product-price').digits();
    $('#product-option h3').digits();
    $('.product-select-item').digits();
    $('#product-total').digits();

    $(".product-bottom .top").click(function(){
        scroll(0,0);
    });
    
    $(window).bind('scroll', function () {
        if ($(window).scrollTop() > 965) {
            $('.product-info-bottom').addClass('fixed');
            $('.product-info-bottom.fixed').css('top', $(this).scrollTop() - 70);
            $('.content .product-menu').css('margin-top', '0');
            // $('.content .product-bottom .tab').css('padding-top', '90px');
        } else {
            $('.product-info-bottom').removeClass('fixed').removeAttr('style');
            $('.content .product-menu').css('margin-top', '0px');
            // $('.content .product-bottom .tab').css('padding-top', '30px');
        }
    });

    $('#detail-info').on('click', function() {
        $('html, body').animate({
            scrollTop: $(".product-detail-info").offset().top - 50
        }, 300);
    });

    $('#use-info').on('click', function() {
        $('html, body').animate({
            scrollTop: $(".product-detail-use").offset().top - 50
        }, 300);
    });

    $('#review-info').on('click', function() {
        $('html, body').animate({
            scrollTop: $(".product-detail-review").offset().top - 50
        }, 300);
    });

    $('#caution-info').on('click', function() {
        $('html, body').animate({
            scrollTop: $(".product-detail-caution").offset().top - 50
        }, 300);
    });
});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};