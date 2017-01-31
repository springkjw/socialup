$(function () {
    $('.price').digits();
});

$('.fa.fa-angle-down').on('click', function () {
    if($(this).attr('aria-hidden')=='true'){
        $(this).parent().next().show();
        $(this).attr('aria-hidden', false);
    }
    else{
        $(this).parent().next().hide();
        $(this).attr('aria-hidden', true);
    }
});

/* gauge part */
$('.table_product_detail').each(function(){
    var color = $(this).attr('data-color');
    var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');
    if(num == 1){
        $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-6px', 'top':'36px', 'transform': 'rotate(18deg)'});
    }
    else if (num==2){
        $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'17px', 'top':'5px', 'transform': 'rotate(45deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'56px', 'top':'-7px', 'transform': 'rotate(90deg)'});
    }
    else if (num == 4){
        $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'93px', 'top':'7px', 'transform': 'rotate(135deg)'});
    }
    else{
        $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'114px', 'top':'36px', 'transform': 'rotate(155deg)'});
    }
});

$('.show_detail_btn.first').on('click', function () {
    if($(this).attr('aria-hidden')=='true'){
        $(this).parent().next().show();
        $(this).attr('aria-hidden', false);
    }
    else{
        $(this).parent().next().hide();
        $(this).attr('aria-hidden', true);
    }
});

$('.show_detail_btn.second').on('click', function () {
    if($(this).attr('aria-hidden')=='true'){
        $(this).parent().next().next().show();
        $(this).attr('aria-hidden', false);
    }
    else{
        $(this).parent().next().next().hide();
        $(this).attr('aria-hidden', true);
    }
});

$('.show_detail_btn.third').on('click', function () {
    if($(this).attr('aria-hidden')=='true'){
        $(this).parent().next().next().next().show();
        $(this).attr('aria-hidden', false);
    }
    else{
        $(this).parent().next().next().next().hide();
        $(this).attr('aria-hidden', true);
    }
});

/* wish-list-modal part */
$('.review').on('click', function () {
    $(this).parent().next().show();
});


$('.review_btn.close').on('click', function () {
    $(this).parent().parent().hide();
});
