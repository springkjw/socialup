
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
    var color  = $('.product-gauge').attr('data-color');
    // $('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({
    //         'background-color': color,
    //         'color': 'white'
    //     });
    var num = $('.circle-wrapper .circle').attr('gauge-data');
    if(num == 1){
        $('.circle-wrapper .circle-list').eq(0).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'-10px', 'top':'78px', 'transform': 'rotate(18deg)'});
    }
    else if (num==2){
        $('.circle-wrapper .circle-list').eq(1).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'31px', 'top':'17px', 'transform': 'rotate(45deg)'});
    }
    else if (num == 3){
        $('.circle-wrapper .circle-list').eq(2).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'100px', 'top':'-10px', 'transform': 'rotate(90deg)'});
    }
    else if (num == 4){
        $('.circle-wrapper .circle-list').eq(3).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'176px', 'top':'14px', 'transform': 'rotate(135deg)'});
    }
    else{
        $('.circle-wrapper .circle-list').eq(4).find('.circle-text').css({'background-color': color, 'color': 'white'});
        $('.circle-wrapper .circle-arrow').css({'position':'relative', 'left':'218px', 'top':'72px', 'transform': 'rotate(155deg)'});
    }
    /* Adding comma */
    $('.cash .cash-price').digits();
    add_manuscript_price_to_total_init();
    add_highrank_price_to_total_init();
    highrank_price_change_for_total();
    manuscript_price_change_for_total();
});


/* add manuscript part */
function manuscript_price_change_for_total() {
    $(".product-select-item.manuscript input").change(function () {
        var previous_total = parseInt(removeComma($('.product-total #product-total').text()));
        var manuscript_price = parseInt(removeComma($('#product-manuscript-price').text()));
        if (this.checked) {
            $('.product-total #product-total').text(previous_total + manuscript_price);
        }
        else {
            $('.product-total #product-total').text(previous_total - manuscript_price);
        }
        $('#product-total').digits();
    });
}


function add_manuscript_price_to_total_init() {
        var previous_total = parseInt(removeComma($('.product-total #product-total').text()));
        var manuscript_price = parseInt(removeComma($('#product-manuscript-price').text()));
        if ($('.product-select-item.manuscript input').is(':checked')) {
            $('.product-total #product-total').text(previous_total + manuscript_price);
        }
        $('#product-total').digits();
}


/* add manuscript part */
function highrank_price_change_for_total(){
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
}


/* add highrank part */
// $(".product-select-item.highrank input").change(function() {
function add_highrank_price_to_total_init() {
    var previous_total = parseInt(removeComma($('.product-total #product-total').text()));
    var highrank_price = parseInt(removeComma($('#product-highrank-price').text()));
    if($('.product-select-item.highrank input').is(':checked')) {
        $('.product-total #product-total').text(previous_total+highrank_price);
    }
    $('#product-total').digits();
}


/* wish-list-modal part */
$('.wish-list-modal-btn-close').on('click', function () {
    $('.wish-list-modal').hide();
})

/* cart-modal part */
$('.cart-confirm-modal-btn-close').on('click', function () {
    $('.cart-confirm-modal').hide();
})