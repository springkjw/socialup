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

var arrow_flag = false;
$('.dropdown').click(function () {
    if (arrow_flag){
        $('.dropdown').css('background-color','white');
        $('.dropdown-content').hide();
        arrow_flag= false;
    }
    else{
        $('.dropdown').css('background-color','#f1f1f1');
        $('.dropdown-content').show();
        arrow_flag= true;
    }
});

$('html').click(function(e) {
    if(!$(e.target).hasClass('dropdown') && $('.dropdown-content').css('display')=='block')
    {
        $('.dropdown').css('background-color','white');
        $('.dropdown-content').hide();
        arrow_flag= false;
    }
});

$('.dropdown-content label').on('click', function () {
    $('.dropdown-selected').html($('.dropdown-content input:checked').parent().text());
    $('.dropdown').css('background-color','white');
    $('.dropdown-content').hide();
});