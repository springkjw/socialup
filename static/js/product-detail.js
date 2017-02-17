
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

    /* seller rating part */
    $('.seller-rating').each(function() {
        var rating = Math.round($(this).attr('data-rating'));
        for (var i = 0; i < rating; i++) {
            $($(this).find('i')).each(function(j) {
                if (i == j) {
                    $(this).addClass('active');
                }
            });
        }
    });

    /* total_rating part */
    var total_rating = Math.round($('.total-rating').attr('data-rating'));
    for (var i = 0; i < total_rating; i++) {
        $($('.total-rating').find('i')).each(function(j) {
            if (i == j) {
                $(this).addClass('active');
            }
        });
    }
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

jQuery.fn.center = function () {
    $(this).css({
        'position' : 'absolute',
        'left' : '50%',
        'top' : '50%',
        'margin-left' : function() {return -$(this).outerWidth()/2},
        'margin-top' : function() {return -$(this).outerHeight()/2}
    });
};

$(document).ready(function(){
    var contents_satisfy = 0;
    var contents_normal = 0;
    var contents_unsatisfy = 0;

    var ads_satisfy = 0;
    var ads_normal = 0;
    var ads_unsatisfy = 0;

    var kindness_satisfy = 0;
    var kindness_normal = 0;
    var kindness_unsatisfy = 0;

    $('.tab-review').each(function(){
        /* contents part */
        var contents = ($(this).find($('.review-satisfiy-sub.contents .review-satisfiy-sub-box')).text());
        contents = contents.replace(/\s+/g, '');
        if(contents=='만족'){
            contents_satisfy +=1;
        }else if(contents=='보통'){
            contents_normal +=1;
        }else{
            contents_unsatisfy +=1;
        }
        /* ads part */
        var ads = ($(this).find($('.review-satisfiy-sub.ads .review-satisfiy-sub-box')).text());
        ads = ads.replace(/\s+/g, '');
        if(ads=='만족'){
            ads_satisfy +=1;
        }else if(ads=='보통'){
            ads_normal +=1;
        }else{
            ads_unsatisfy +=1;
        }
        /* kindness part */
        var kindness = ($(this).find($('.review-satisfiy-sub.kindness .review-satisfiy-sub-box')).text());
        kindness = kindness.replace(/\s+/g, '');
        if(kindness=='만족'){
            kindness_satisfy +=1;
        }else if(kindness=='보통'){
            kindness_normal +=1;
        }else{
            kindness_unsatisfy +=1;
        }
    });
    var contents_total = contents_satisfy + contents_normal + contents_unsatisfy;
    var ads_total = ads_satisfy + ads_normal + ads_unsatisfy;
    var kindness_total = kindness_satisfy + kindness_normal + kindness_unsatisfy;
    var calculated_contents_satisfy = (contents_satisfy/contents_total)*100;
    var calculated_contents_normal = (contents_normal/contents_total)*100;
    var calculated_contents_unsatisfy = (contents_unsatisfy/contents_total)*100;
    var calculated_ads_satisfy = (ads_satisfy/ads_total)*100;
    var calculated_ads_normal = (ads_normal/ads_total)*100;
    var calculated_ads_unsatisfy = (ads_unsatisfy/ads_total)*100;
    var calculated_kindness_satisfy = (kindness_satisfy/kindness_total)*100;
    var calculated_kindness_normal = (kindness_normal/kindness_total)*100;
    var calculated_kindness_unsatisfy = (kindness_unsatisfy/kindness_total)*100;
    $('.graph-part.contents span:nth-child(1)').css('width', calculated_contents_satisfy + '%');
    $('.graph-part.contents .graph-text li:nth-child(1)').css('width', calculated_contents_satisfy -1 + '%');
    $('.graph-part.contents .graph-text li:nth-child(1)').text('만족 (' + parseInt(calculated_contents_satisfy) + '%)');
    $('.graph-part.contents span:nth-child(2)').css('width', calculated_contents_normal + '%');
    $('.graph-part.contents .graph-text li:nth-child(2)').css('width', calculated_contents_normal -1 + '%');
    $('.graph-part.contents .graph-text li:nth-child(2)').text('보통 (' + parseInt(calculated_contents_normal) + '%)');
    $('.graph-part.contents span:nth-child(3)').css('width', calculated_contents_unsatisfy + '%');
    $('.graph-part.contents .graph-text li:nth-child(3)').css('width', calculated_contents_unsatisfy -1 + '%');
    $('.graph-part.contents .graph-text li:nth-child(3)').text('불만족 (' + parseInt(calculated_contents_unsatisfy) + '%)');
    if(parseInt(calculated_contents_normal)<18 && parseInt(calculated_contents_normal)>0){
        var temp_num = (17-calculated_contents_normal)/2 + 1;
        $('.graph-part.contents .graph-text li:nth-child(1)').css('width', calculated_contents_satisfy -1 - temp_num + '%');
        $('.graph-part.contents .graph-text li:nth-child(2)').css('width', 17 + '%');
        $('.graph-part.contents .graph-text li:nth-child(3)').css('width', calculated_contents_unsatisfy -1 -temp_num + '%');
    }
    if(parseInt(calculated_contents_satisfy)<18 && parseInt(calculated_contents_satisfy)>0){
        var temp_num = (17-calculated_contents_satisfy)/2 + 1;
        $('.graph-part.contents .graph-text li:nth-child(1)').css('width', 17 + '%');
        $('.graph-part.contents .graph-text li:nth-child(2)').css('width', calculated_contents_normal-1 -temp_num + '%');
        $('.graph-part.contents .graph-text li:nth-child(3)').css('width', calculated_contents_unsatisfy-1 -temp_num + '%');
    }
    if(parseInt(calculated_contents_unsatisfy)<22 && parseInt(calculated_contents_unsatisfy)>0){
        var temp_num = (21-calculated_contents_unsatisfy)/2 + 2;
        $('.graph-part.contents .graph-text li:nth-child(1)').css('width', calculated_contents_satisfy - temp_num + '%');
        $('.graph-part.contents .graph-text li:nth-child(2)').css('width', calculated_contents_normal - temp_num + '%');
        $('.graph-part.contents .graph-text li:nth-child(3)').css('width', 21 + '%');
        $('.graph-part.contents .graph-text li:nth-child(3)').css('float', 'right');
    }
    $('.graph-part.ads span:nth-child(1)').css('width', calculated_ads_satisfy + '%');
    $('.graph-part.ads .graph-text li:nth-child(1)').css('width', calculated_ads_satisfy -1 + '%');
    $('.graph-part.ads .graph-text li:nth-child(1)').text('만족 (' + parseInt(calculated_ads_satisfy) + '%)');
    $('.graph-part.ads span:nth-child(2)').css('width', calculated_ads_normal*100 + '%');
    $('.graph-part.ads .graph-text li:nth-child(2)').css('width', calculated_ads_normal -1 + '%');
    $('.graph-part.ads .graph-text li:nth-child(2)').text('보통 (' + parseInt(calculated_ads_normal) + '%)');
    $('.graph-part.ads span:nth-child(3)').css('width', calculated_ads_unsatisfy + '%');
    $('.graph-part.ads .graph-text li:nth-child(3)').css('width', calculated_ads_unsatisfy -1 + '%');
    $('.graph-part.ads .graph-text li:nth-child(3)').text('불만족 (' + parseInt(calculated_ads_unsatisfy) + '%)');
    if(parseInt(calculated_ads_satisfy)<18 && parseInt(calculated_ads_satisfy)>0){
        var temp_num = (17-calculated_ads_satisfy)/2 + 2;
        $('.graph-part.ads .graph-text li:nth-child(1)').css('width', 17 + '%');
        $('.graph-part.ads .graph-text li:nth-child(2)').css('width', calculated_ads_normal -0.5 -temp_num + '%');
        $('.graph-part.ads .graph-text li:nth-child(3)').css('width', calculated_ads_unsatisfy -0.5 -temp_num + '%');
    }
    if(parseInt(calculated_ads_normal)<18 && parseInt(calculated_ads_normal)>0){
        var temp_num = (17-calculated_ads_normal)/2 + 2;
        $('.graph-part.ads .graph-text li:nth-child(1)').css('width', calculated_ads_satisfy -0.5 - temp_num + '%');
        $('.graph-part.ads .graph-text li:nth-child(2)').css('width', 17 + '%');
        $('.graph-part.ads .graph-text li:nth-child(3)').css('width', calculated_ads_unsatisfy -0.5 -temp_num + '%');
    }
    if(parseInt(calculated_ads_unsatisfy)<22 && parseInt(calculated_ads_unsatisfy)>0){
        var temp_num = (21-calculated_ads_unsatisfy)/2 + 2;
        $('.graph-part.ads .graph-text li:nth-child(1)').css('width', calculated_ads_satisfy -2 - temp_num + '%');
        $('.graph-part.ads .graph-text li:nth-child(2)').css('width', calculated_ads_normal -2 - temp_num + '%');
        $('.graph-part.ads .graph-text li:nth-child(3)').css('width', 21 + '%');
        $('.graph-part.ads .graph-text li:nth-child(3)').css('float', 'right');
    }
    $('.graph-part.kindness span:nth-child(1)').css('width', calculated_kindness_satisfy + '%');
    $('.graph-part.kindness .graph-text li:nth-child(1)').css('width', calculated_kindness_satisfy -1 + '%');
    $('.graph-part.kindness .graph-text li:nth-child(1)').text('만족 (' + parseInt(calculated_kindness_satisfy) + '%)');
    $('.graph-part.kindness span:nth-child(2)').css('width', calculated_kindness_normal + '%');
    $('.graph-part.kindness .graph-text li:nth-child(2)').css('width', calculated_kindness_normal -1 + '%');
    $('.graph-part.kindness .graph-text li:nth-child(2)').text('보통 (' + parseInt(calculated_kindness_normal) + '%)');
    $('.graph-part.kindness span:nth-child(3)').css('width', calculated_kindness_unsatisfy + '%');
    $('.graph-part.kindness .graph-text li:nth-child(3)').css('width', calculated_kindness_unsatisfy -1 + '%');
    $('.graph-part.kindness .graph-text li:nth-child(3)').text('불만족 (' + parseInt(calculated_kindness_unsatisfy) + '%)');
    if(parseInt(calculated_kindness_satisfy)<18 && parseInt(calculated_kindness_satisfy)>0){
        var temp_num = (17-calculated_kindness_satisfy)/2 +2;
        $('.graph-part.kindness .graph-text li:nth-child(1)').css('width', 17 + '%');
        $('.graph-part.kindness .graph-text li:nth-child(2)').css('width', calculated_kindness_normal -1 -temp_num + '%');
        $('.graph-part.kindness .graph-text li:nth-child(3)').css('width', calculated_kindness_unsatisfy -1 -temp_num + '%');
    }
    if(parseInt(calculated_kindness_normal)<18 && parseInt(calculated_kindness_normal)>0){
        var temp_num = (17-calculated_kindness_normal)/2 +2;
        $('.graph-part.kindness .graph-text li:nth-child(1)').css('width', calculated_kindness_satisfy -1 - temp_num + '%');
        $('.graph-part.kindness .graph-text li:nth-child(2)').css('width', 17 + '%');
        $('.graph-part.kindness .graph-text li:nth-child(3)').css('width', calculated_kindness_unsatisfy -1 -temp_num + '%');
    }
    if(parseInt(calculated_kindness_unsatisfy)<22 && parseInt(calculated_kindness_unsatisfy)>0){
        var temp_num = (21-parseInt(calculated_kindness_unsatisfy))/2 + 3;
        $('.graph-part.kindness .graph-text li:nth-child(1)').css('width', calculated_kindness_satisfy -1 - temp_num + '%');
        $('.graph-part.kindness .graph-text li:nth-child(2)').css('width', calculated_kindness_normal -1 - temp_num + '%');
        $('.graph-part.kindness .graph-text li:nth-child(3)').css('width', 21 + '%');
        $('.graph-part.kindness .graph-text li:nth-child(3)').css('float', 'right');
    }
    $('.graph-text li').each(function(){
        if($(this).css('width')=='0px'){
            $(this).hide();
        }
    });
});