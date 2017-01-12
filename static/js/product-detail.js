
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

/* car-modal part */
$('.cart-confirm-modal-btn-close').on('click', function () {
    $('.cart-confirm-modal').hide();
})