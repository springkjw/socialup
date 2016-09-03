$(function() {
    var header_menu = $('.header-dropdown');
    var header_profile = $('#header-profile');

    header_profile.on('click', function() {
        if(header_menu.css('display') == 'none') {
            header_menu.css('display', 'block');
        }else {
            header_menu.css('display', 'none');
        }
    });

    $(window).click(function(e) {
        if(!header_menu.is(e.target) && header_menu.has(e.target).length === 0) {
            if(!header_profile.is(e.target) && header_profile.has(e.target).length === 0) {
                header_menu.css('display', 'none');
            }
        }
    });
});