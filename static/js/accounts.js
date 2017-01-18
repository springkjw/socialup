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
})

/*
$(document).ready(function(){
             alert('hi');
         });
    */