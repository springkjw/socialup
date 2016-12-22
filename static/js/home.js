$(function() {
    $('.checkbox .step1').on('click', '.survey-checkbox', step1Check);
    $('.checkbox .step2').on('click', '.survey-checkbox', step2Check);
    $('.checkbox .step3').on('click', '.survey-checkbox', step3Check);
    $('.survey').on('click', 'img.fa-angle-right', nextStep);
    $('.survey').on('click', 'img.fa-angle-left', prevStep);

    $('.list-card').each(function() {
        var rating_ele = $(this).find('.card-author-info-rating');
        var rating = Math.round(rating_ele.attr('data-rating'));
        for (var i = 0; i < rating; i++) {
            $(rating_ele.find('i')).each(function(j) {
                if (i == j) {
                    $(this).addClass('active');
                }
            });
        }
    });

    $('.card-price').digits();

    // socialup gauge
    Highcharts.setOptions({
        lang: {
            thousandsSep: ','
        }
    });
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['48%', '60%'],
            size: '100%',
            startAngle: -110,
            endAngle: 110,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '75%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        // the value axis
        yAxis: {
            showFirstLabel: false,
            showLastLabel: false,
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            title: {
                y: -70
            },
            labels: {
                y: 0
            }
        },
        plotOptions: {
            solidgauge: {
                innerRadius: '75%',
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    $('.socialup-gauge').each(function() {
        var color = $(this).attr('data-color');

        $(this).highcharts(Highcharts.merge(gaugeOptions, {
            yAxis: {
                min: 0,
                max: 100,
                stops: [
                    [1, color],
                ],
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'socialup-guage',
                data: [89],
                dataLabels: {
                    format: '<div style="text-align:center;margin-top: -30px;"><span style="font-size:24px;color:' +
                        color + '">{point.y:,.0f}</span>' +
                        '<span style="font-size:10px;color:' + color + '">%</span></div>'
                },
            }]

        }));
    });
});

$.fn.digits = function() {
    return this.each(function() {
        $(this).text($(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
    })
};

function step1Check() {
    if ($(this).attr('id') === 'survey-all') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step1 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step1 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step1 #survey-all').prop('checked', false);
        }
    }
}

function step2Check() {
    if ($(this).attr('id') === 'survey-all-age') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step2 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step2 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step2 #survey-all-age').prop('checked', false);
        }
    }
}

function step3Check() {
    if ($(this).attr('id') === 'survey-all-type') {
        if ($(this).is(":checked") === true) {
            $('.checkbox .step3 input:checkbox').each(function() {
                $(this).prop('checked', true);
            });
        } else {
            $('.checkbox .step3 input:checkbox').each(function() {
                $(this).prop('checked', false);
            });
        }
    } else {
        if ($(this).is(":checked") === false) {
            $('.checkbox .step3 #survey-all-type').prop('checked', false);
        }
    }
}

var survey_count = 0;

function nextStep() {
    if (survey_count == 0) {
        $('.survey .fa-angle-left').fadeIn();
        $('.steps.step1').css('display', 'none');
        $('.steps.step2').fadeIn().animate({
            right: '54%'
        }, {
            duration: 'slow',
            queue: false
        });
        $('.sub-title-step1').css('display', 'none');
        $('.sub-title-step2').fadeIn();

        $('.survey-pagination .p-step1').removeClass('active');
        $('.survey-pagination .p-step2').addClass('active');

        survey_count++;
    } else if (survey_count == 1) {
        $('.survey .fa-angle-right').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step3').fadeIn().animate({
            right: '54%'
        }, {
            duration: 'slow',
            queue: false
        });
        $('.sub-title-step2').css('display', 'none');
        $('.sub-title-step3').fadeIn();

        $('.survey-pagination .p-step2').removeClass('active');
        $('.survey-pagination .p-step3').addClass('active');

        $('.survey-complete').fadeIn();

        survey_count++;
    }
}

function prevStep() {
    if (survey_count == 1) {
        $('.survey .fa-angle-left').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step1').fadeIn();
        $('.sub-title-step1').fadeIn();
        $('.sub-title-step2').css('display', 'none');

        $('.survey-pagination .p-step1').addClass('active');
        $('.survey-pagination .p-step2').removeClass('active');

        survey_count--;
    } else if (survey_count == 2) {
        $('.survey .fa-angle-right').fadeIn();
        $('.steps.step3').css('display', 'none');
        $('.steps.step2').fadeIn();
        $('.sub-title-step2').fadeIn();
        $('.sub-title-step3').css('display', 'none');

        $('.survey-pagination .p-step2').addClass('active');
        $('.survey-pagination .p-step3').removeClass('active');

        $('.survey-complete').css('display', 'none');

        survey_count--;
    }
}
