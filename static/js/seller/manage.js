$(function () {
    $('.dashboard-item-more').on('click', '.fa-angle-down', function () {
        $(this).parent().parent().find('.dashboard-item-popup').show();
        $(this).removeClass('fa-angle-down').addClass('fa-angle-up');
    });

    $('.dashboard-item-more').on('click', '.fa-angle-up', function () {
        $(this).parent().parent().find('.dashboard-item-popup').hide();
        $(this).removeClass('fa-angle-up').addClass('fa-angle-down');
    });
});

/* gauge part */
$('.item_top_image').each(function(){
    var color = $(this).attr('data-color');
    $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
    var num = 1;
    if(num == 1){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'5px', 'top':'36px', 'transform': 'rotate(18deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'26%', 'top':'-7px', 'transform': 'rotate(90deg)'});
    }
});

function order_item_count(){

}