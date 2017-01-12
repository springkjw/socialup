
$('#product-price').digits(); 
$('#product-option h3').digits();
$('#product-manuscript-price').digits(); 
$('#product-highrank-price').digits(); 
$('#product-total').digits();
$('.price-sub').digits();

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};

function removeComma(str){
    return str.split(',').join('');
}

$(document).ready(function() {
    /* gauge part */
    var count = 0;
    var color  = $('.product-gauge').attr('data-color');
    $('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({
            'background-color': color,
            'color': 'white'
        });
    var num = 1;
    if (num == 1) {
        $('.circle-wrapper .circle-arrow').css({
            'position': 'relative',
            'left': '-10px',
            'top': '78px',
            'transform': 'rotate(18deg)'
        });
    }
    else if (num == 3) {
        $('.circle-wrapper .circle-arrow').css({
            'position': 'relative',
            'left': '33%',
            'top': '-7px',
            'transform': 'rotate(90deg)'
        });
    }
    /* Adding comma */
    var cash  = parseInt($('.cash span').text());
    cash = AddComma(cash);
    $('.cash span').text(cash + '원~');
});

function AddComma(data_value) {
    return Number(data_value).toLocaleString('en');
}

/* add manuscript part */
$(".product-select-item.manuscript input").change(function() {
    var previous_total = parseInt(removeComma($('.product-total #product-total').text()));
    var manuscript_price = parseInt(removeComma($('#product-manuscript-price').text()));
    if(this.checked) {
        $('.product-total #product-total').text(previous_total+manuscript_price);
    }
    else{
        $('.product-total #product-total').text(previous_total-manuscript_price);
    }
            $('#product-total').digits();
});

/* add manuscript part */
$(".product-select-item.highrank input").change(function() {
    var previous_total = parseInt(removeComma($('.product-total #product-total').text()));
    var highrank_price = parseInt(removeComma($('#product-highrank-price').text()));
    if(this.checked) {
        $('.product-total #product-total').text(previous_total+highrank_price);
    }
    else{
        $('.product-total #product-total').text(previous_total-highrank_price);
    }
            $('#product-total').digits();
});

function heart_on_off(){

}