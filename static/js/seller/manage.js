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
    var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');
    if(num == 1){
        $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'3px', 'top':'37px', 'transform': 'rotate(18deg)'});
    }
    else if (num==2){
        $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'29px', 'top':'6px', 'transform': 'rotate(45deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'64px', 'top':'-6px', 'transform': 'rotate(90deg)'});
    }
    else if (num == 4){
        $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'102px', 'top':'7px', 'transform': 'rotate(135deg)'});
    }
    else{
        $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'124px', 'top':'35px', 'transform': 'rotate(155deg)'});
    }
});

/* prodcut_delete modal */
$('.product_btn.delete').on('click', function(){
    $(this).parent().prev().show();
    $(this).parent().prev().center();
});

$('.delete-confirm-modal-btn.yes').on('click',function(){
    $(this).parent().parent().next().submit();
});

$('.delete-confirm-modal-btn.no').on('click',function() {
    $(this).parent().parent().hide();
});

jQuery.fn.center = function () {
    $(this).css({
        'position' : 'fixed',
        'left' : '50%',
        'top' : '40%',
        'margin-left' : function() {return -$(this).outerWidth()/2},
        'margin-top' : function() {return -$(this).outerHeight()/2}
    });
};