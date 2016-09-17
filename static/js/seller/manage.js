$(function () {
    $('.dashboard-item-more').on('click', '.fa-angle-down', function () {
        $(this).parent().parent().find('.dashboard-item-popup').show();
        $(this).removeClass('fa-angle-down').addClass('fa-angle-up');
    });

    $('.dashboard-item-more').on('click', '.fa-angle-up', function () {
        $(this).parent().parent().find('.dashboard-item-popup').hide();
        $(this).removeClass('fa-angle-up').addClass('fa-angle-down');
    });
});