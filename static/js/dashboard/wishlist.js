$(function() {
    var rating_ele = $('.dashboard-wishlist-item-rating');

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

    $('.dashboard-wishlist-item-more').on('click', '.fa-angle-down', function() {
        $(this).parent().parent().find('.dashboard-wishlist-item-popup').show();
        $(this).removeClass('fa-angle-down').addClass('fa-angle-up');
    });

    $('.dashboard-wishlist-item-more').on('click', '.fa-angle-up', function() {
        $(this).parent().parent().find('.dashboard-wishlist-item-popup').hide();
        $(this).removeClass('fa-angle-up').addClass('fa-angle-down');
    });

    $('#wishlist-price').digits();
});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};

/* gauge part */
$('.card-main-info').each(function(){
    var color = $(this).attr('data-color');
    $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
    var num = 1;
    if(num == 1){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-10px', 'top':'40px', 'transform': 'rotate(18deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'26%', 'top':'-7px', 'transform': 'rotate(90deg)'});
    }
});