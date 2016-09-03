$(function () {
    $('.auth-agreement').on('click', '.fa-caret-down', function () {
        $(this).parent().parent().parent().find('.auth-agreement-content').show();
        $(this).removeClass('fa-caret-down').addClass('fa-caret-up');
    });

    $('.auth-agreement').on('click', '.fa-caret-up', function () {
        $(this).parent().parent().parent().find('.auth-agreement-content').hide();
        $(this).removeClass('fa-caret-up').addClass('fa-caret-down');
    });

    $('.auth-area .signup button').on('click', function () {
        var email = $('#id_email').val();
        var pwd1 = $('#id_password1').val();
        var pwd2 = $('#id_password2').val();

        if (!$('#agreenment1').is(":checked") || !$('#agreenment2').is(":checked")) {
            alert('약관에 동의해주세요.');
        }
    });
});