var statuses = {};

$(function () {
    // 전체 목록에서 각 상태 별로 숫자세기..
    $('.order-list-table tr[data-status]').each(function(i, el) {
        var status = $(el).data('status');
        if (statuses.hasOwnProperty(status))
            statuses[status] += 1;
        else
            statuses[status] = 1;
    });

    // 상단 상태버튼들 안의 괄호에 숫자 채워넣기..
    $('.order-list-nav li[data-status]').each(function(i, el) {
        var status = $(el).data('status');
        if (statuses.hasOwnProperty(status))
            $(this).children('span.status-count').html('' + statuses[status]);
        else
            $(this).children('span.status-count').html('0');
    });

    // 상단 상태버튼을 눌렀을 때의 처리..
    $('.order-list-nav ul li').click(function() {
        $('.order-list-nav ul li').removeClass('active');
        $(this).addClass('active');

        if ($(this).data('status')) {
            $('.order-list-table tbody tr').hide();
            $('.order-list-table tbody tr[data-status="{}"]'.format($(this).data('status'))).show();
        } else {
            $('.order-list-table tbody tr').show();
        }
    });

    // 전체 선택 버튼을 눌렀을 경우..
    $('.order-list-table th input[type="checkbox"]').change(function() {
        $('.order-list-table td input[type="checkbox"]').prop('checked', this.checked);
    });
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

/* popups */

$(".dialog-order-list.process").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('.order-mange-form-process.active').submit();
            }
        },
        {
            text: "취소",
            click: function() {
                $('.order-mange-form-process').each(function(){
                    $(this).removeClass('active');
                });
                $(this).dialog('close');
            }
        }
        ]
    });

$(".dialog-order-list.wait_confirm").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('.order-mange-form-wait_confirm.active').submit();
            }
        },
        {
            text: "취소",
            click: function() {
                $('.order-mange-form-wait_confirm').each(function(){
                    $(this).removeClass('active');
                });
                $(this).dialog('close');
            }
        }
        ]
    });

$(".dialog-order-list.cancel").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('.order-mange-form-cancel.active').submit();
            }
        },
        {
            text: "취소",
            click: function() {
                $('.order-mange-form-cancel').each(function(){
                    $(this).removeClass('active');
                });
                $(this).dialog('close');
            }
        }
        ]
    });

$('.detail_bottom_btn.process').on('click', function() {
    $(this).parent().addClass('active');
    $(".dialog-order-list.process").dialog('open');
});

$('.detail_bottom_btn.wait_confirm').on('click', function() {
    $(this).parent().addClass('active');
    $(".dialog-order-list.wait_confirm").dialog('open');
});

$('.detail_bottom_btn.cancel').on('click', function() {
    $(this).parent().addClass('active');
    $(".dialog-order-list.cancel").dialog('open');
});