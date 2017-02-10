/* for version2 */

$(document).ready(function(){
    color_unchecked_sns_type();
    color_checked_sns_type();
    sns_type_color();
    color_checked_additional_info();
    sns_additional_info_color();
    color_checked_sex();
    sex_color();
    tag_func();
    check_tags_for_hover();
    check_sns_type_for_display();
});



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
function tag_func(){
    $('#product-upload-form input[name=tag]').on('change', function() {
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
    });
    checked_before_clicked.forEach(function(val){
        jQuery(val).css({'display':'none'});
    });
    checked_clicked.forEach(function(val) {
        jQuery(val).css({'display': 'inline-block'});
    });
}

function uncheck_tags_for_hover(){
    $('input[name=tag]').each(function(){
        $(this).prop('checked',false);
    });
}

/* this is for hide additional_inform, sex
 * additional_inform for facebook
  * sex for instagram */
function check_sns_type_for_display(){
    if($('#id_sns_type_0').is(":checked")){
        //blog
        $('.product-upload-info.additional_info').css('display','none');
        $('.product-upload-info.sex').css('display','none');
        $('.product-upload-sub.follower_visit_num').css('display','inline');
        $('.product-upload-sub.follower_num').css('display','inline');
        $('.product-upload-sub.follower_friends_num').css('display','none');
        $('.product-upload-sub.highrank').css('display','block');

   }
   else if($('#id_sns_type_1').is(":checked")){
        //facebook
        $('.product-upload-info.additional_info').css('display','block');
        $('.product-upload-info.sex').css('display','none');
        $('.product-upload-sub.follower_visit_num').css('display','none');
        $('.product-upload-sub.follower_num').css('display','inline');
        $('.product-upload-sub.follower_friends_num').css('display','inline');
        $('.product-upload-sub.highrank').css('display','none');

   }
   else if($('#id_sns_type_2').is(":checked")) {
        //instagram
        $('.product-upload-info.additional_info').css('display','none');
        $('.product-upload-info.sex').css('display','block');
        $('.product-upload-sub.follower_visit_num').css('display','none');
        $('.product-upload-sub.follower_num').css('display','block');
        $('.product-upload-sub.follower_friends_num').css('display','none');
        $('.product-upload-sub.highrank').css('display','none');

   }
   else if($('#id_sns_type_3').is(":checked")) {
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

function check_facebook_type_for_display(){
    if($('#id_sns_additional_info_1').is(":checked")){
        $('.product-upload-sub.follower_friends_num').css('display','none');
    }else{
        $('.product-upload-sub.follower_friends_num').css('display','inline');
    }
}

$('#product-upload-form .product-upload-info.additional_info input').on('change', function() {
    check_facebook_type_for_display();
});


$(function () {
    $("form").on("submit", function(event) { event.stopPropagation(); });

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


});

function submit_form(){
    console.log('submit_form');
    $('#product-upload-form').submit();
    console.log('submit_form done');
}

function set_input_value(selector, new_val){
    $(selector).val(new_val);
}

/* product_edit confirm */
$("#dialog-confirm2").dialog({
    resizable: false,
    height:190,
    autoOpen: false,
    width: 330,
    modal: true,
    buttons: [
        {
            text: "확인",
            click: function() {
                $('#product-upload-form').submit();
            }
        }
        ]
    });

$('.final_edit').on('click', function() {
    $("#dialog-confirm2").dialog('open');
});

/* product_upload len check */
$('#id_oneline_intro').on('keyup', function() {
    if($(this).val().length > 26) {
        alert('한줄소개는 26자이내로 입력해주세요.')
        $(this).val($(this).val().substring(0, 26));
    }
});