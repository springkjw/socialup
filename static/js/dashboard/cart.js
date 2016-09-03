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