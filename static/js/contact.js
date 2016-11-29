$(document).ready(function () {
    $('.contact').scrollToFixed({
        bottom: 0,
        limit: $('footer').offset().top - 60
    });

    $('.contact').hover(function () {
        $('.contact .contact-drop-down').stop(true, false, true).slideToggle(300);
    });
});