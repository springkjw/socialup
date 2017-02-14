$('.question_nav li button').click(function () {
    $(this).parent().parent().find('button').removeClass("active");
    $(this).addClass("active");
    var question_type = $(this).attr('question-type');
    if(question_type=='entire'){
        $('.question_content').each(function(){
            $(this).show();
        });
        $('.question_content .question_content_each').each(function(){

        });
        var num_index = $('.question_content_each').length/10;
        $('#paging').empty();
        if(num_index >1) {
            for (i = 1; i <= num_index + 1; i++) {
                $('#paging').append('<li class="paging_num">' + i + '</li>');
            }
            ;
            paging(10);
            $('#paging li.paging_num:first').addClass('active');
        }
    }else{
        $('.question_content').each(function(){
            $(this).hide();
        });
        $('.question_content.'+question_type).show();
        $('.question_content.'+question_type+' .question_content_each').each(function(){
            $(this).show();
        });
        var num_index = $('.question_content.'+question_type+' .question_content_each').length/10;
        $('#paging').empty();
        if(num_index >1){
            for (i = 1; i <= num_index+1; i++){
                $('#paging').append('<li class="paging_num">'+i+'</li>');
            };
            paging(10);
            $('#paging li.paging_num:first').addClass('active');
        }
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
    paging(10);
    $('#paging li.paging_num:first').addClass('active');
});

function paging(param_count){
    count = 1;
    $('.question_content_each').each(function(){
        if(param_count-10<count && count<=param_count){
            $(this).show();
        }else{
            $(this).hide();
        }
        count++;
    });
};

$('#paging').on('click', 'li.paging_num', function(){
    $('#paging li.paging_num').each(function(){
        $(this).removeClass('active');
    });
    var temp = $(this).text();
    $(this).addClass('active');
    temp = Number(temp)*10;
    paging(temp);
});