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