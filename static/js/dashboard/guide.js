$('.question_nav li button').click(function () {
    $(this).parent().parent().find('button').removeClass("active");
    $(this).addClass("active");
    var question_type = $(this).attr('question-type');
    if(question_type=='entire'){
        $('.question_content').each(function(){
            $(this).show();
        });
    }else{
        $('.question_content').each(function(){
            $(this).hide();
        });
        $('.question_content.'+question_type).show();
    }
});

$(function () {
    $('.question_content_each').on('click', '.fa-caret-down', function () {
        $(this).parent().parent().parent().find('.question_content_text').show();
        $(this).removeClass('fa-caret-down').addClass('fa-caret-up');
    });

    $('.question_content_each').on('click', '.fa-caret-up', function () {
        $(this).parent().parent().parent().find('.question_content_text').hide();
        $(this).removeClass('fa-caret-up').addClass('fa-caret-down');
    });
});
