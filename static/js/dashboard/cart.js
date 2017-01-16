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
    $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
    var num = 1;
    if(num == 1){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-15px', 'top':'38px', 'transform': 'rotate(18deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'26%', 'top':'-7px', 'transform': 'rotate(90deg)'});
    }
});