$('.guide-nav li #guide_btn').click(function () {
    $(this).parent().addClass( "active" );
    $(this).parent().next().removeClass( "active" );
});

$('.guide-nav li #question_btn').click(function () {
    $(this).parent().addClass( "active" );
    $(this).parent().prev().removeClass( "active" );
});

$(function () {
    $('.question_content_each').on('click', '.fa-caret-down', function () {
        $(this).parent().parent().parent().find('.question_content_text').show();
        $(this).removeClass('fa-caret-down').addClass('fa-caret-up');
    });

    $('.question_content_each').on('click', '.fa-caret-up', function () {
        $(this).parent().parent().parent().find('.question_content_text').hide();
        $(this).removeClass('fa-caret-up').addClass('fa-caret-down');
    });

    $('#product-upload-form').submit(function () {
        if($('#agreenment1').length==0){
            return true;
        }
        else{
            if (!$('#agreenment1').is(":checked")) {
               alert('약관에 동의해주세요.');
               return false;
            }else{
                return true;
            }
        }
    });
});