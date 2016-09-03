$(function() {
    $('.checkbox .step1').on('click', '.survey-checkbox', step1Check);
    $('.checkbox .step2').on('click', '.survey-checkbox', step2Check);
    $('.checkbox .step3').on('click', '.survey-checkbox', step3Check);
    $('.survey').on('click', 'img.fa-angle-right', nextStep);
    $('.survey').on('click', 'img.fa-angle-left', prevStep);

    $('.list-card').each(function() {
        var rating_ele = $(this).find('.card-author-info-rating');
        var rating = Math.round(rating_ele.attr('data-rating'));
        for(var i=0; i<rating; i++) {
            $(rating_ele.find('i')).each(function(j) {
                if(i == j) {
                    $(this).addClass('active');
                }
            });
        }
    });

    $('.card-price').digits();
});

$.fn.digits = function(){
    return this.each(function(){
        $(this).text( $(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") );
    })
};

function step1Check() {
    if($(this).attr('id') === 'survey-all') {
        if($(this).is(":checked") === true) {
            $('.checkbox .step1 input:checkbox').each(function () {
                $(this).prop('checked', true);
            });
        }else{
            $('.checkbox .step1 input:checkbox').each(function () {
                $(this).prop('checked', false);
            });
        }
    }else {
        if($(this).is(":checked") === false) {
            $('.checkbox .step1 #survey-all').prop('checked', false);
        }
    }
}

function step2Check() {
    if($(this).attr('id') === 'survey-all-age') {
        if($(this).is(":checked") === true) {
            $('.checkbox .step2 input:checkbox').each(function () {
                $(this).prop('checked', true);
            });
        }else{
            $('.checkbox .step2 input:checkbox').each(function () {
                $(this).prop('checked', false);
            });
        }
    }else {
        if($(this).is(":checked") === false) {
            $('.checkbox .step2 #survey-all-age').prop('checked', false);
        }
    }
}

function step3Check() {
    if($(this).attr('id') === 'survey-all-type') {
        if($(this).is(":checked") === true) {
            $('.checkbox .step3 input:checkbox').each(function () {
                $(this).prop('checked', true);
            });
        }else{
            $('.checkbox .step3 input:checkbox').each(function () {
                $(this).prop('checked', false);
            });
        }
    }else {
        if($(this).is(":checked") === false) {
            $('.checkbox .step3 #survey-all-type').prop('checked', false);
        }
    }
}

var survey_count = 0;

function nextStep() {
    if(survey_count == 0) {
        $('.survey .fa-angle-left').fadeIn();
        $('.steps.step1').css('display', 'none');
        $('.steps.step2').fadeIn().animate(
            {right: '54%'},
            {duration: 'slow', queue: false}
        );
        $('.sub-title-step1').css('display', 'none');
        $('.sub-title-step2').fadeIn();

        $('.survey-pagination .p-step1').removeClass('active');
        $('.survey-pagination .p-step2').addClass('active');

        survey_count++;
    }else if(survey_count == 1) {
        $('.survey .fa-angle-right').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step3').fadeIn().animate(
            {right: '54%'},
            {duration: 'slow', queue: false}
        );
        $('.sub-title-step2').css('display', 'none');
        $('.sub-title-step3').fadeIn();

        $('.survey-pagination .p-step2').removeClass('active');
        $('.survey-pagination .p-step3').addClass('active');

        $('.survey-complete').fadeIn();

        survey_count++;
    }
}

function prevStep() {
    if(survey_count == 1) {
        $('.survey .fa-angle-left').fadeOut();
        $('.steps.step2').css('display', 'none');
        $('.steps.step1').fadeIn();
        $('.sub-title-step1').fadeIn();
        $('.sub-title-step2').css('display', 'none');

        $('.survey-pagination .p-step1').addClass('active');
        $('.survey-pagination .p-step2').removeClass('active');

        survey_count--;
    }else if(survey_count ==2) {
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