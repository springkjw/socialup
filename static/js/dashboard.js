$(function() {
    $('.dashboard-side .user-money-number').digits();
    $('.dashboard-point').digits();

});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};