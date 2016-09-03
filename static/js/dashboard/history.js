$(function() {
    $('.history-current-point h2').digits();
    $('.dashboard-history-table .history-amount-c').digits();

    $('.dashboard-history-title .history-large').on('click', function() {
        $(this).parent().find('.history-large').removeClass('active');
        $(this).addClass('active');
        $('.dashboard-history-table').removeClass('active');

        var text = $(this).text().replace(/ /g,'').replace(/(\r\n|\n|\r)/gm,'')

        if(text == '충전') {
            $('.charge-history').addClass('active');
        }else if(text == '사용') {
            $('.use-history').addClass('active');
        }else {

        }

    });

    var d = new Date();
    //set today date
    setToday(d);
    //set one month
    setOneMonth(d);

    $('.dashboard-period-button-group .one_month').on('click', function() {
        var d = new Date();
        setOneMonth(d);
        $(this).parent().find('.dashboard-period-button').removeClass('active');
        $(this).addClass('active');
    });

    $('.dashboard-period-button-group .three_month').on('click', function() {
        var d = new Date();
        setTreeMonth(d);
        $(this).parent().find('.dashboard-period-button').removeClass('active');
        $(this).addClass('active');
    });

    $('.dashboard-period-button-group .six_month').on('click', function() {
        var d = new Date();
        setSixMonth(d);
        $(this).parent().find('.dashboard-period-button').removeClass('active');
        $(this).addClass('active');
    });

    $('.dashboard-period-button-group .twelve_month').on('click', function() {
        var d = new Date();
        setTwelveMonth(d);
        $(this).parent().find('.dashboard-period-button').removeClass('active');
        $(this).addClass('active');
    });
});

function setToday(d) {
    $('.dashboard-period-input-group').find('#end_date').val(formatDate(d));
}

function setOneMonth(d) {
    d.setMonth(d.getMonth() - 1);
    $('.dashboard-period-input-group').find('#start_date').val(formatDate(d));
}

function setTreeMonth(d) {
    d.setMonth(d.getMonth() - 3);
    $('.dashboard-period-input-group').find('#start_date').val(formatDate(d));
}

function setSixMonth(d) {
    d.setMonth(d.getMonth() - 6);
    $('.dashboard-period-input-group').find('#start_date').val(formatDate(d));
}

function setTwelveMonth(d) {
    d.setMonth(d.getMonth() - 12);
    $('.dashboard-period-input-group').find('#start_date').val(formatDate(d));
}

function formatDate(d) {
    var month = d.getMonth() + 1;
    var day = d.getDate();

    output = d.getFullYear() + '.' +
        (month < 10 ? '0' : '') + month + '.' +
        (day < 10 ? '0' : '') + day;

    return output;
}