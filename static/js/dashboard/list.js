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

$('.table_product_detail_bottom .review').on('click', function () {
    $(this).parent().parent().parent().parent().prev().show();
});

$('.review_btn.submit').on('click', function () {
    value = parseFloat($(this).parent().find("input:radio[name='rating']:checked").val()).toFixed(1);
    if (isNaN(value))
        alert("만족도 평가에 체크해주세요");
    else
        $(this).parent().find('.hidden_submit').click();
});

$('.review_btn.close').on('click', function () {
    $(this).parent().parent().hide();
});

$(".dialog-purchase-list.decide").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('.order-item-decide-from.active').submit();
            }
        },
        {
            text: "취소",
            click: function() {
                $('.order-item-decide-from').each(function(){
                    $(this).removeClass('active');
                });
                $(this).dialog('close');
            }
        }
        ]
    });

$(".dialog-purchase-list.cancel").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('.order-item-cancel-from.active').submit();
            }
        },
        {
            text: "취소",
            click: function() {
                $('.order-item-cancel-from').each(function(){
                    $(this).removeClass('active');
                });
                $(this).dialog('close');
            }
        }
        ]
    });

$('.detail_bottom_btn.decide').on('click', function() {
    $(this).parent().addClass('active');
    $(".dialog-purchase-list.decide").dialog('open');
});

$('.detail_bottom_btn.cancel').on('click', function() {
    $(this).parent().addClass('active');
    $(".dialog-purchase-list.cancel").dialog('open');
});