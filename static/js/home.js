$(function() {
    $('.checkbox .step1').on('click', '.survey-checkbox', step1Check);
    $('.checkbox .step2').on('click', '.survey-checkbox', step2Check);
    $('.checkbox .step3').on('click', '.survey-checkbox', step3Check);
    $('.survey').on('click', 'img.fa-angle-right', nextStep);
    $('.survey').on('click', 'img.fa-angle-left', prevStep);

    $('.list-card').each(function() {
        var rating_ele = $(this).find('.card-author-info-rating');
        var rating = Math.round(rating_ele.attr('data-rating'));
        for (var i = 0; i < rating; i++) {
            $(rating_ele.find('i')).each(function(j) {
                if (i == j) {
                    $(this).addClass('active');
                }
            });
        }
    });

    $('.card-price').digits();
    /*
    // socialup gauge
    Highcharts.setOptions({
        lang: {
            thousandsSep: ','
        }
    });
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['48%', '60%'],
            size: '100%',
            startAngle: -110,
            endAngle: 110,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '75%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        // the value axis
        yAxis: {
            showFirstLabel: false,
            showLastLabel: false,
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            title: {
                y: -70
            },
            labels: {
                y: 0
            }
        },
        plotOptions: {
            solidgauge: {
                innerRadius: '75%',
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    $('.socialup-gauge').each(function() {
        var color = $(this).attr('data-color');

        $(this).highcharts(Highcharts.merge(gaugeOptions, {
            yAxis: {
                min: 0,
                max: 100,
                stops: [
                    [1, color],
                ],
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'socialup-guage',
                data: [89],
                dataLabels: {
                    format: '<div style="text-align:center;margin-top: -30px;"><span style="font-size:24px;color:' +
                        color + '">{point.y:,.0f}</span>' +
                        '<span style="font-size:10px;color:' + color + '">%</span></div>'
                },
            }]

        }));
    });
    */
});

$(document).ready(function(){
    /* gauge part */
    $('.card-main-info').each(function(){
        var color = $(this).attr('data-color');
        var num = $(this).find('.circle-wrapper .circle').attr('gauge-data');

        if(num == 1){
            $(this).find('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-10px', 'top':'60px', 'transform': 'rotate(18deg)'});
        }
        else if (num==2){
            $(this).find('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'24px', 'top':'13px', 'transform': 'rotate(45deg)'});
        }
        else if (num == 3){
            $(this).find('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'79px', 'top':'-7px', 'transform': 'rotate(90deg)'});
        }
        else if (num == 4){
            $(this).find('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'136px', 'top':'12px', 'transform': 'rotate(135deg)'});
        }
        else{
            $(this).find('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
            $(this).find('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'167px', 'top':'56px', 'transform': 'rotate(155deg)'});
        }
    });
    $('.cash .cash-price').digits();
    /* range part */
    $( function() {

    });
    /* tag part start */
    tag_func();
});

//function filter_ajax(min, max){
//    var real_min = min;
//    var real_max = max;
//    $('#loading').css("display", "block");
//    setTimeout(function() {
//        $.ajax({url: "/", success: function(result){
//            $(".list-card").each(function (){
//                var temp_text = $(this).find('.cash span').attr("data-price");
//                temp_text = parseInt(temp_text);
//                if(real_min <= temp_text && temp_text <= real_max) {
//                    $(this).css("display", "inline-block");
//                }else{
//                    $(this).css("display", "none");
//                }
//            });
//            $('#loading').css("display","none");
//        }});
//    },1000);
//
//    /*
//    */
//}

$.fn.digits = function() {
    return this.each(function() {
        $(this).text($(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
    })
};

/* home jumbotron_right func */
function right_zero(){
    $('.jumbotron_right.zero').hide();
    $('.jumbotron_right.first').css('display','inline-block');
};

function right_first(){
    $('.jumbotron_right.first').hide();
    $('.jumbotron_right.second').css('display','inline-block');
};

function right_second(){
    $('.jumbotron_right.second').hide();
    $('.jumbotron_right.third').css('display','inline-block');
};

function right_third(){
    $('.jumbotron_right.third').hide();
    $('.jumbotron_right.fourth').css('display','inline-block');
};

function right_fourth(){
    $('.jumbotron_right.fourth').hide();
    $('.jumbotron_right.fifth').css('display','inline-block');
};

function right_fifth(){
    $('.jumbotron_right.fifth').hide();
    $('.jumbotron_right.first').css('display','inline-block');
};





function step1Check() {
    if ($(this).attr('id') === 'survey-all') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step1 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step1 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step1 #survey-all').prop('checked', false);
        }
    }
}

function step2Check() {
    if ($(this).attr('id') === 'survey-all-age') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step2 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step2 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step2 #survey-all-age').prop('checked', false);
        }
    }
}

function step3Check() {
    if ($(this).attr('id') === 'survey-all-type') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step3 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step3 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step3 #survey-all-type').prop('checked', false);
        }
    }
}

var survey_count = 0;

function nextStep() {
    if (survey_count == 0) {
        $('.survey .fa-angle-left').fadeIn();
        $('.steps.step1').css('display', 'none');
        $('.steps.step2').fadeIn().animate({
            right: '54%'
        }, {
            duration: 'slow',
            queue: false
        });
        $('.sub-title-step1').css('display', 'none');
        $('.sub-title-step2').fadeIn();

        $('.survey-pagination .p-step1').removeClass('active');
        $('.survey-pagination .p-step2').addClass('active');

        survey_count++;
    } else if (survey_count == 1) {
        $('.survey .fa-angle-right').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step3').fadeIn().animate({
            right: '54%'
        }, {
            duration: 'slow',
            queue: false
        });
        $('.sub-title-step2').css('display', 'none');
        $('.sub-title-step3').fadeIn();

        $('.survey-pagination .p-step2').removeClass('active');
        $('.survey-pagination .p-step3').addClass('active');

        $('.survey-complete').fadeIn();

        survey_count++;
    }
}

function prevStep() {
    if (survey_count == 1) {
        $('.survey .fa-angle-left').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step1').fadeIn();
        $('.sub-title-step1').fadeIn();
        $('.sub-title-step2').css('display', 'none');

        $('.survey-pagination .p-step1').addClass('active');
        $('.survey-pagination .p-step2').removeClass('active');

        survey_count--;
    } else if (survey_count == 2) {
        $('.survey .fa-angle-right').fadeIn();
        $('.steps.step3').css('display', 'none');
        $('.steps.step2').fadeIn();
        $('.sub-title-step2').fadeIn();
        $('.sub-title-step3').css('display', 'none');

        $('.survey-pagination .p-step2').addClass('active');
        $('.survey-pagination .p-step3').removeClass('active');

        $('.survey-complete').css('display', 'none');

        survey_count--;
    }
}


/* This is for tag */

function tag_func(){
    $('#tag_navigation input[name=tag]').on('change', function() {
        check_tags_for_hover();
    });
}

function check_tags_for_hover(){
    var checked_clicked = $('input[name=tag]:checked').next().find('.tag_image_clicked').get();
    var checked_before_clicked = $('input[name=tag]:checked').next().find('.tag_image_before_click').get();
    var unchecked_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_clicked').get();
    var unchecked_before_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_before_click').get();

    if(checked_clicked.length>6) {
        var clicked_input = jQuery(event.target);
        clicked_input.prop('checked',false);
        // 변경한 사항 다시 array에 저장
        checked_clicked = $('input[name=tag]:checked').next().find('.tag_image_clicked').get();
        checked_before_clicked = $('input[name=tag]:checked').next().find('.tag_image_before_click').get();
        unchecked_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_clicked').get();
        unchecked_before_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_before_click').get();
        alert('포스팅가능 분야는 최대 6개까지 선택 가능합니다.');
    }

    var clicked_input = jQuery(event.target);
    if(clicked_input.prop('value')=='all' && !(clicked_input.is(':not(:checked)'))){
        $('input[name=tag]').prop('checked', false);
        $('input[value=all]').prop('checked', true);
        checked_clicked = $('input[name=tag]:checked').next().find('.tag_image_clicked').get();
        checked_before_clicked = $('input[name=tag]:checked').next().find('.tag_image_before_click').get();
        unchecked_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_clicked').get();
        unchecked_before_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_before_click').get();
    }
    else if($('input[name=tag]:not([value=all]):checked').length){
        $('input[value=all]').prop('checked', false);
        checked_clicked = $('input[name=tag]:checked').next().find('.tag_image_clicked').get();
        checked_before_clicked = $('input[name=tag]:checked').next().find('.tag_image_before_click').get();
        unchecked_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_clicked').get();
        unchecked_before_clicked = $('input[name=tag]:not(:checked)').next().find('.tag_image_before_click').get();
    }

    // display attr 조정해서 이미지 바꿔주기
    unchecked_clicked.forEach(function(val){
        jQuery(val).css({'display':'none'});
    });
    unchecked_before_clicked.forEach(function(val){
        jQuery(val).css({'display':'inline-block'});
        jQuery(val).parent().parent().css('border', 'none');
    });
    checked_before_clicked.forEach(function(val){
        jQuery(val).css({'display':'none'});
    });
    checked_clicked.forEach(function(val){
        jQuery(val).css({'display': 'inline-block'});
        jQuery(val).parent().parent().css('border-bottom', '1px solid #648efc');
    });
}