$(document).ready(function() {

    /* gauge part */
    $('.card-main-info').each(function(){
        var color = $(this).attr('data-color');
        $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        var num = 1;
        if(num == 1){
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-13px', 'top':'41px', 'transform': 'rotate(18deg)'});
        }
        else if (num == 3){
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'26%', 'top':'-7px', 'transform': 'rotate(90deg)'});
        }
    });
});