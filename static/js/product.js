$(function () {
    var price_ = $('.price');
    var variation_total = $('#id_variation_set-TOTAL_FORMS');

    // $('.variation_price').autoNumeric('init', {
    //     vMin: '0',
    //     mDec: 0,
    //     lZero: 'deny',
    //     wEmpty: 'zero'
    // });

    // set variation total num is 1
    variation_total.val(1);


    // set summer-note initial height
    $('panel-body').css('height', '400px');

    // trigger post image
    $('.post_image').on('click', function () {
        $('#id_image').trigger('click');
    });

    // image input file is change
    $('#id_image').change(function () {
        readImage(this);
    });

    //checking variation option item is filled
    $('.price-option-area input').on('blur', function () {

    });
    $('#id_variation_set-1-price').blur(function () {
        if ($(this).val() == '') {
            variation_total.val(1);
        } else {
            variation_total.val(2);
        }
    });

    $('#id_variation_set-1-title').blur(function () {
        if ($(this).val() == '') {
            variation_total.val(1);
        } else {
            variation_total.val(2);
        }
    });

    $('#id_variation_set-1-day').blur(function () {
        if ($(this).val() == '') {
            variation_total.val(1);
        } else {
            variation_total.val(2);
        }
    });

    $('#id_variation_set-0-is_default').attr('checked', 'true');

    $('#id_variation_set-0-price').attr('placehoder', '10,000원 이상, 1,000원 단위로 가능');

    var subject_all_html = '<label for="id_all"><input id="id_all" name="tag" type="checkbox" value="">전체</label>';

    price_.on('click', '.add_option', function () {
        var nxt_num = $('.price-option-area').length + 1;
        $('#id_variation_set-TOTAL_FORMS').val(nxt_num + 1);

        var price_html = '<div class="price-option-area">' +
            '<div class="form-input">' +
            '<input class="variation_price" id="id_variation_set-' + nxt_num + '-price"' +
            'name="variation_set-' + nxt_num + '-price" placeholder="옵션의 추가 비용"> ' +
            '<label>원 추가시</label>' +
            '</div>' +
            '<div class="form-input">' +
            '<input class="variation_title" id="id_variation_set-' + nxt_num + '-title"' +
            'name="variation_set-' + nxt_num + '-title" placeholder="추가 비용을 지불 시 제공하는 상품 내용">' +
            '</div>' +
            '<div class="form-input">' +
            '<input class="variation_day" id="id_variation_set-' + nxt_num + '-day"' +
            'name="variation_set-' + nxt_num + '-day" placeholder="옵션 구매 시 추가 일수">' +
            '<label>일 추가</label>' +
            '</div>' +
            '<div class="options minus">' +
            '<i class="fa fa-minus" aria-hidden="true"></i>' +
            '</div>' +
            '</div>';

        if (nxt_num == 1) {
            $(price_html).insertAfter($('.price .step3_button'));
        } else {
            $(price_html).insertAfter($('.price .form-area .price-option-area').last());
        }
    });

    price_.on('click', '.minus', function () {
        $(this).parent().remove();
        var price_field = $('.price-option-area');

        var total_num = price_field.length;
        $('#id_variation_set-TOTAL_FORMS').val(total_num + 1);
        price_field.each(function (index) {
            $(this).find('input').each(function () {
                var ele_id = $(this).attr('id').split('-');
                if (ele_id.length == 3) {
                    var new_id = ele_id[0] + '-' + (index + 1).toString() + '-' + ele_id[2];
                    $(this).attr('id', new_id);
                }
                var ele_name = $(this).attr('name').split('-');
                if (ele_name.length == 3) {
                    var new_name = ele_id[0] + '-' + (index + 1).toString() + '-' + ele_id[2];
                    $(this).attr('name', new_name);
                }
            });
        });
    });

    $('.buttons .start').on('click', function () {
        var step = $.trim($('.step_num.active .title').text());
        $('.step_num').removeClass('active');

        if (step == 'STEP1') {
            check_step1();
        } else if (step == 'STEP2') {
            check_step2();
        }
    });

    $('.form-right').on('click', '.add_url', function () {
        var url_html = '<br/><div class="form-url-input add-url-input">' +
            '<input id="id_url" name="url" type="text">' +
            '<div class="button minus">-</div>' +
            '</div>';

        $(url_html).insertAfter($('.form-url-input').last());
    });

    $('.form-right').on('click', '.minus', function () {
        $(this).parent().prev().remove();
        $(this).parent().remove();
    });

    $('.step_num').on('click', function () {
        var step = $(this).attr('id');
        $('.step_num').removeClass('active');

        if (step == 'step1_') {
            $('.step_num#step1_').addClass('active');

            $('.step1').show();
            $('.step2').hide();
            $('.step3').hide();

            $('.step_num#step2_').removeClass('active');
            $('.step_num#step3_').removeClass('active');

            $('.buttons .final').hide();
            $('.buttons .start').show();
        } else if (step == 'step2_') {
            check_step1();
        } else if (step == 'step3_') {
            check_step2();
        }

    });

});

function readImage(input) {
    if (input.files && input.files[0]) {
        var image = new FileReader();

        image.onload = function (e) {
            $('#post_image').attr('src', e.target.result);
        };

        image.readAsDataURL(input.files[0]);

        $('#default_image').hide();
        $('.post_image h2').hide();
    }
}

function check_step1() {
    $('.step_num#step1_').addClass('active');
    if (!$('#id_title').val()) {
        alert('제목을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_title').offset().top - 60
        }, 300);
        $('#id_title').focus();
    } else if (!$('#id_url').val()) {
        alert('SNS 주소를 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_url').offset().top - 60
        }, 300);
        $('#id_url').focus();
    } else if (!$('#id_influence').val()) {
        alert('SNS 영향력을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_influence').offset().top - 60
        }, 300);
        $('#id_influence').focus();
    } else if (!$('#id_image').val() && !$('#post_image').attr('src')) {
        alert('메인 이미지를 등록해주세요.');
        $('html, body').animate({
            scrollTop: $('#post_image').offset().top - 60
        }, 300);
    } else if (!$('input[name="type"]').is(":checked")) {
        alert('광고 가능한 SNS 종류를 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else if (!$('input[name="tag"]').is(":checked")) {
        alert('주로 다루는 주제를 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else if (!$('input[name="target"]').is(":checked")) {
        alert('주로 참여하는 타겟층을 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else {
        $('.step1').hide().removeClass('active');
        $('.step2').show().addClass('active');
        $('.step3').hide().removeClass('active');

        $('.step_num#step1_').removeClass('active');
        $('.step_num#step2_').addClass('active');
        $('.step_num#step3_').removeClass('active');

        $('.buttons .final').hide();
        $('.buttons .start').show();
    }
}

function check_step2() {
    //$('.step_num#step2_').addClass('active');
    //
    //if (!$('#id_required').val()) {
    //    alert('유의사항을 입력해주세요.');
    //    $('html, body').animate({
    //        scrollTop: $('#id_required').offset().top - 60
    //    }, 300);
    //    $('#id_required').focus();
    //} else if (!$('#id_command').val()) {
    //    alert('지시사항을 입력해주세요.');
    //    $('html, body').animate({
    //        scrollTop: $('#id_command').offset().top - 60
    //    }, 300);
    //    $('#id_command').focus();
    //} else if (!$('#id_refund').val()) {
    //    alert('환불 규정을 입력해주세요.');
    //    $('html, body').animate({
    //        scrollTop: $('#id_refund').offset().top - 60
    //    }, 300);
    //    $('#id_refund').focus();
    //} else if (!$('#id_description').val()) {
    //    alert('상품 상세 내용을 입력해주세요.');
    //    $('html, body').animate({
    //        scrollTop: $('#id_description').offset().top - 60
    //    }, 300);
    //    $('#id_description').focus();
    //} else {
    $('.step1').hide().removeClass('active');
    $('.step2').hide().removeClass('active');
    $('.step3').show().addClass('active');

    $('.step_num#step1_').removeClass('active');
    $('.step_num#step2_').removeClass('active');
    $('.step_num#step3_').addClass('active');

    $('.buttons .final').show();
    $('.buttons .start').hide();
    //}
}


/* this is for sns_type_color */


function sns_type_color(){
    $('#product-upload-form input').on('change', function() {
        color_unchecked_sns_type();
        color_checked_sns_type();
    });
}

function color_unchecked_sns_type() {
    $('input[name=sns_type][type="radio"]', '#product-upload-form').parent().css(
           {'color': '#a3a3a3',
            'border': 'solid 1px #a3a3a3',
            'background-color':'white'
           }
   );
}
function color_checked_sns_type(){
    $('input[name=sns_type]:checked', '#product-upload-form').parent().css(
           {'background-color':'#648efc',
            'color': 'white',
            'border': 'solid 1px #648efc'}
    );
}


$(document).ready(function(){
    color_unchecked_sns_type();
    color_checked_sns_type();
    sns_type_color();
    color_checked_additional_info();
    sns_additional_info_color();
    color_checked_sex();
    sex_color();
});

/* this is for sns_additional_info_color */

function sns_additional_info_color() {
    $('#product-upload-form input').on('change', function () {
        color_unchecked_additional_info();
        color_checked_additional_info();
    });
}

function color_checked_additional_info(){
    $('input[name=sns_additional_info]:checked', '#product-upload-form').parent().css(
       {'background-color':'#648efc',
        'color': 'white',
        'border': 'solid 1px #648efc'}
   );
}

function color_unchecked_additional_info(){
    $('input[name=sns_additional_info][type="radio"]', '#product-upload-form').parent().css(
       {'color': '#a3a3a3',
        'border': 'solid 1px #a3a3a3',
        'background-color':'white'
       }
   );
}


/* this is for sex_color */
function sex_color(){
    $('#product-upload-form input').on('change', function() {
        color_unchecked_sex();
        color_checked_sex();
    });
}

function color_checked_sex(){
    $('input[name=sex]:checked', '#product-upload-form').parent().css(
       {'background-color':'#648efc',
        'color': 'white',
        'border': 'solid 1px #648efc'}
   );
}

function color_unchecked_sex(){
    $('input[name=sex][type="radio"]', '#product-upload-form').parent().css(
       {'color': '#a3a3a3',
        'border': 'solid 1px #a3a3a3',
        'background-color':'white'
       }
   );
}



/* this is for tag */
$('#product-upload-form input[name=tag]').on('change', function() {
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
    // display attr 조정해서 이미지 바꿔주기
    unchecked_clicked.forEach(function(val){
        jQuery(val).css({'display':'none'});
    });
    unchecked_before_clicked.forEach(function(val){
        jQuery(val).css({'display':'inline-block'});
    });
    checked_before_clicked.forEach(function(val){
        jQuery(val).css({'display':'none'});
    });
    checked_clicked.forEach(function(val) {
        jQuery(val).css({'display': 'inline-block'});
    });
});

/* this is for hide additional_inform, sex
 * additional_inform for facebook
  * sex for instagram */
function check_sns_type_for_display(){
    if($('#id_sns_type_0').is(":checked")){
        console.log('blog');
        //blog
        $('.product-upload-info.additional_info').css('display','none');
        $('.product-upload-info.sex').css('display','none');
        $('.product-upload-sub.follower_visit_num').css('display','inline');
        $('.product-upload-sub.follower_num').css('display','inline');
        $('.product-upload-sub.follower_friends_num').css('display','none');
        $('.product-upload-sub.highrank').css('display','block');

   }
   else if($('#id_sns_type_1').is(":checked")){
        console.log('facebook');
        //facebook
        $('.product-upload-info.additional_info').css('display','block');
        $('.product-upload-info.sex').css('display','none');
        $('.product-upload-sub.follower_visit_num').css('display','none');
        $('.product-upload-sub.follower_num').css('display','inline');
        $('.product-upload-sub.follower_friends_num').css('display','inline');
        $('.product-upload-sub.highrank').css('display','none');

   }
   else if($('#id_sns_type_2').is(":checked")) {
        console.log('instagram');
        //instagram
        $('.product-upload-info.additional_info').css('display','none');
        $('.product-upload-info.sex').css('display','block');
        $('.product-upload-sub.follower_visit_num').css('display','none');
        $('.product-upload-sub.follower_num').css('display','block');
        $('.product-upload-sub.follower_friends_num').css('display','none');
        $('.product-upload-sub.highrank').css('display','block');

   }
   else if($('#id_sns_type_3').is(":checked")) {
        console.log('kakaostory');
        //kakaostory
        $('.product-upload-info.additional_info').css('display','none');
        $('.product-upload-info.sex').css('display','none');
        $('.product-upload-sub.follower_visit_num').css('display','none');
        $('.product-upload-sub.follower_num').css('display','block');
        $('.product-upload-sub.follower_friends_num').css('display','none');
        $('.product-upload-sub.highrank').css('display','none');
   }
}

$('#product-upload-form input').on('change', function() {
    check_sns_type_for_display();
});



$(function () {
    $('.auth-agreement').on('click', '.fa-caret-down', function () {
        jQuery($(this).parent().prev().get(0)).text('다음사항에 동의합니다.');
        $(this).parent().parent().parent().find('.auth-agreement-content').show();
        $(this).removeClass('fa-caret-down').addClass('fa-caret-up');
    });

    $('.auth-agreement').on('click', '.fa-caret-up', function () {
        jQuery($(this).parent().prev().get(0)).text('이용약관에 동의합니다.');
        $(this).parent().parent().parent().find('.auth-agreement-content').hide();
        $(this).removeClass('fa-caret-up').addClass('fa-caret-down');
    });

    $('#product-upload-form').submit(function () {
        if (!$('#agreenment1').is(":checked")) {
            alert('약관에 동의해주세요.');
            return false;
        }else{
            return true;
        }
    });
});

function set_input_value(selector, new_val){
    $(selector).val(new_val);
}

/* product_edit product_previous select part
$(function(){
    $.ajax({url: "/", success: function(result){
        alert($("#previous_proudcts_select option:selected").val());
    }});
});


$( "#previous_proudcts_select" ).change(function() {
    var temp = $("#previous_proudcts_select option:selected").val();
    //alert($("#previous_proudcts_select option:selected").val());
    $.ajax({url: "/", success: function(result){
    }});
});
    */