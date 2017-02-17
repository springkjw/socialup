$(document).ready(function() {

    /* rating part */
    var seller_rating_ele = $('.seller-rating');
    var rating = Math.round(seller_rating_ele.attr('data-rating'));
    for(var i=0; i<rating; i++) {
        $(seller_rating_ele.find('i')).each(function(j) {
            if(i == j) {
                $(this).addClass('active');
            }
        });
    }

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

    /* gauge part */
    $('.card-main-info').each(function(){
        var color = $(this).attr('data-color');
        var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');
        if(num == 1){
            $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-11px', 'top':'41px', 'transform': 'rotate(18deg)'});
        }
        else if (num==2){
            $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'10px', 'top':'12px', 'transform': 'rotate(45deg)'});
        }
        else if (num == 3){
            $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'48px', 'top':'-2px', 'transform': 'rotate(90deg)'});
        }
        else if (num == 4){
            $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'85px', 'top':'12px', 'transform': 'rotate(135deg)'});
        }
        else{
            $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'106px', 'top':'43px', 'transform': 'rotate(160deg)'});
        }
    });

    var temp = $('.seller_rating_ratio').attr('data-rating');
    temp = Math.round(temp)
    $('#rating-num').text(temp);
});