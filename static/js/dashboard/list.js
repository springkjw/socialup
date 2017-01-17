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
    $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
    var num = 1;
    if(num == 1){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-10px', 'top':'35px', 'transform': 'rotate(18deg)'});
    }
    else if (num == 3){
        $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'26%', 'top':'-7px', 'transform': 'rotate(90deg)'});
    }
});

$('.show_detail_btn').on('click', function () {
    if($(this).attr('aria-hidden')=='true'){
        $(this).parent().next().show();
        $(this).attr('aria-hidden', false);
    }
    else{
        $(this).parent().next().hide();
        $(this).attr('aria-hidden', true);
    }
});