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