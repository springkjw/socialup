$(function () {
    var IMP = window.IMP;
    IMP.init('imp68762150');

    $('.billing-info .total h1').digits();
    $('.item .item-price h2').digits();
    $('.mileage .button span').digits();
    $('.point .button span').digits();

    $('.pay-info .discount input').each(function () {
        $(this).autoNumeric('init', {
            vMin: '0',
            vMax: $(this).attr('data-max'),
            mDec: 0,
            lZero: 'deny',
            wEmpty: 'zero'
        });
    });

    $('.pay-info .pay-option input[type="radio"]').on('click', function () {
        $('.buyer-info').show();
    });

    $('.buyer-info input[name="phone"]').mask("000-0000-0000");
});