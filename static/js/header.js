$(function () {
    var header_menu = $('.header-dropdown');
    var header_profile = $('#header-profile');

    header_profile.on('click', function () {
        if (header_menu.css('display') == 'none') {
            header_menu.css('display', 'block');
        } else {
            header_menu.css('display', 'none');
        }
    });

    $(window).click(function (e) {
        if (!header_menu.is(e.target) && header_menu.has(e.target).length === 0) {
            if (!header_profile.is(e.target) && header_profile.has(e.target).length === 0) {
                $('.header-menu').removeClass('active').find('span').find('i').removeClass('fa-caret-up').addClass('fa-caret-down');
                header_menu.css('display', 'none');
            }
        }
    });

    $('.header-dropdown .header-menu').on('click', function () {
        $('.header-menu').removeClass('active').find('span').find('i').removeClass('fa-caret-up').addClass('fa-caret-down');
        $(this).addClass('active');
        $(this).find('span').find('i').removeClass('fa-caret-down').addClass('fa-caret-up');
    });

    $('#header #money').digits();
});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};