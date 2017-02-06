$(function () {
    $('.add_image').on('click', function () {
        $('#id_media').trigger('click');
    });

    $('#id_media').change(function () {
        readImage(this);
    });
});

function readImage(input) {
    if (input.files && input.files[0]) {
        var image = new FileReader();

        image.onload = function (e) {
            $('.image img').attr('src', e.target.result);
        };

        image.readAsDataURL(input.files[0])
    }
}

$('.change_button').on('click', function () {
    if($('#new_passwd1').val() != $('#new_passwd2').val()){
        alert('변경할 비밀번호가 다릅니다.');
        window.location.reload();
    }
});


/* transition div by button click (basic_info, seller_info) */
$('#btn_basic_info').on('click', function(){
    $('.dashboard-change-form.base').show();
    $('.dashboard-change-form.seller').hide();
    $('#btn_basic_info').css('color','#648efc');
    $('#btn_seller_info').css('color', 'black');
});

$('#btn_seller_info').on('click', function(){
    $('.dashboard-change-form.base').hide();
    $('.dashboard-change-form.seller').show();
    $('#btn_basic_info').css('color','black');
    $('#btn_seller_info').css('color', '#648efc');
});

// file_upload part
$(document).ready(function(){
    var fileTarget = $('#id_business_license');
    fileTarget.on('change', function(){ // 값이 변경되면
        if(window.FileReader){ // modern browser
            var filename = $(this)[0].files[0].name;
        }
        else { // old IE
            var filename = $(this).val().split('/').pop().split('\\').pop(); // 파일명만 추출
        }
        // 추출한 파일명 삽입
        $(this).siblings('.file_name.business_license').val(filename);
    });

    var fileTarget2 = $('#id_account_copy');
    fileTarget2.on('change', function(){ // 값이 변경되면
        if(window.FileReader){ // modern browser
            var filename2 = $(this)[0].files[0].name;
        }
        else { // old IE
            var filename2 = $(this).val().split('/').pop().split('\\').pop(); // 파일명만 추출
        }
        // 추출한 파일명 삽입
        $(this).siblings('.file_name.account_copy').val(filename2);
    });


    $("#dialog-confirm").dialog({
        resizable: false,
        height:190,
        autoOpen: false,
        width: 330,
        modal: true,
        buttons: [
            {
                text: "예",
                click: function() {
                    $('#go_main').val('True');
                    $('#change_form_user').submit();
                }
            },
            {
                text: "아니오",
                click: function() {
                    $('#go_main').val('False');
                    $('#change_form_user').submit();
                }
            }
        ]
    });

    $('.change_button').on('click', function() {
        $("#dialog-confirm").dialog('open');
    });

    $("#dialog-confirm2").dialog({
        resizable: false,
        height:190,
        autoOpen: false,
        width: 330,
        modal: true,
        buttons: [
            {
                text: "예",
                click: function() {
                    $('#go_main2').val('True');
                    $('#change_form_seller').submit();
                }
            },
            {
                text: "아니오",
                click: function() {
                    $('#go_main2').val('False');
                    $('#change_form_seller').submit();
                }
            }
        ]
    });

    $('.change_button_seller').on('click', function() {
        $("#dialog-confirm2").dialog('open');
    });

});


$(document).ready(function() {
    $('.seller_form_input.type input').on('change', function(){
        show_by_seller_type();
    });
});

function show_by_seller_type(){
    if($('#id_type_0').is(":checked")){
        $('.seller_form_content.company_name').hide();
        $('.seller_form_content.representative_name').hide();
        $('.seller_form_content.corporate_number').hide();
        $('.seller_form_content.business_field').hide();
        $('.seller_form_content.company_type').hide();
        $('.seller_form_content.business_license').hide();
        $('.seller_form_content.account_copy').hide();
    }else{
        $('.seller_form_content').show();
    }
}