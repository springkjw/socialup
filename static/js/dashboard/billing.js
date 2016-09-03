$(function () {
    var IMP = window.IMP;
    IMP.init('imp68762150');

    $('#etc-money').find('input[type="tel"]').autoNumeric('init', {
        vMin: '0',
        mDec: 0,
        lZero: 'deny',
        wEmpty: 'zero'
    });

    $('.billing-more').on("click", function () {
        $(this).hide();
        var etc_money = $('#etc-money');
        etc_money.css('display', 'block').find('input:radio[name="amount"]').prop('checked', true);
        etc_money.find('input[type="tel"]').focus();

        amount = 0;
        var total = (Math.round(parseInt(amount) * 1.1)).toString();
        var total_ele = $('.dashboard-charge-total #total');
        total_ele.html('');
        total_ele.html(total + '원');
        total_ele.digits();
    });

    $('#etc-money').on('click', function () {
        $(this).find('input:radio[name="amount"]').prop('checked', true);

        amount = $('#etc-money').find('input[type="tel"]').autoNumeric('get');
        var total = (Math.round(parseInt(amount) * 1.1)).toString();
        var total_ele = $('.dashboard-charge-total #total');
        total_ele.html('');
        total_ele.html(total + '원');
        total_ele.digits();
    });

    $('#etc-money input[type="tel"]').on('keyup', function () {
        amount = $(this).autoNumeric('get');
        var total = (Math.round(parseInt(amount) * 1.1)).toString();
        var total_ele = $('.dashboard-charge-total #total');
        total_ele.html('');
        total_ele.html(total + '원');
        total_ele.digits();
    });

    var amount = null;
    $("input[name='amount']").click(function () {
        if (!$(this).parent().find('input[type="tel"]').length) {
            amount = this.value;
            var total = (Math.round(parseInt(amount) * 1.1)).toString();
            var total_ele = $('.dashboard-charge-total #total');
            total_ele.html('');
            total_ele.html(total + '원');
            total_ele.digits();
        }
    });

    $('.dashboard-charge-info #phone').mask("000-0000-0000");
});

