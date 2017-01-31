$(function() {
    $('.dashboard-cart-item-more').on('click', '.fa-angle-down', function() {
        $(this).parent().parent().find('.dashboard-cart-item-popup').show();
        $(this).removeClass('fa-angle-down').addClass('fa-angle-up');
    });

    $('.dashboard-cart-item-more').on('click', '.fa-angle-up', function() {
        $(this).parent().parent().find('.dashboard-cart-item-popup').hide();
        $(this).removeClass('fa-angle-up').addClass('fa-angle-down');
    });

    $('.dashboard-cart-subtotal #money').digits();

    $('.dashboard-cart .item-money').digits();
});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};

/* gauge part */
$('.dashboard-cart-item').each(function(){
    var color = $(this).attr('data-color');
    var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');
    if(num == 1){
        $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-12px', 'top':'38px', 'transform': 'rotate(18deg)'});
    }
    else if (num==2){
        $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'12px', 'top':'8px', 'transform': 'rotate(45deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'47px', 'top':'-6px', 'transform': 'rotate(90deg)'});
    }
    else if (num == 4){
        $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'84px', 'top':'9px', 'transform': 'rotate(135deg)'});
    }
    else{
        $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'105px', 'top':'38px', 'transform': 'rotate(155deg)'});
    }
});