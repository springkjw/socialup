$(document).ready(function () {
    $('.contact').hover(function () {
        $('.contact .contact-drop-down').stop(true, false, true).slideToggle(300);
    });
});