$(function() {
    var rating_ele = $('.card-author-info-rating');
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
    var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');
    if(num == 1){
        $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-5px', 'top':'39px', 'transform': 'rotate(18deg)'});
    }
    else if (num==2){
        $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'20px', 'top':'10px', 'transform': 'rotate(45deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'57px', 'top':'-3px', 'transform': 'rotate(90deg)'});
    }
    else if (num == 4){
        $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'95px', 'top':'12px', 'transform': 'rotate(135deg)'});
    }
    else{
        $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'118px', 'top':'40px', 'transform': 'rotate(155deg)'});
    }
});