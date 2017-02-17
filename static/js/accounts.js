$(function () {
    $('.add_image').on('click', function () {
        $('#id_media').trigger('click');
    });

    $('#id_media').change(function () {
        readImage(this);
    });
});

function readImage(input) {
    if (input.files && input.files[0]) {
        var image = new FileReader();

        image.onload = function (e) {
            // $('.image img').attr('src', e.target.result);
            $('.base_info_image img').attr('src', e.target.result);
        };

        image.readAsDataURL(input.files[0])
    }
}

$('.change_button').on('click', function () {
    if($('#new_passwd1').val() != $('#new_passwd2').val()){
        alert('변경할 비밀번호가 다릅니다.');
        window.location.reload();
    }
});


/* transition div by button click (basic_info, seller_info) */
$('#btn_basic_info').on('click', function(){
    $('.dashboard-change-form.base').show();
    $('.dashboard-change-form.seller').hide();
    $('#btn_basic_info').css('color','#648efc');
    $('#btn_seller_info').css('color', 'black');
});

$('#btn_seller_info').on('click', function(){
    $('.dashboard-change-form.base').hide();
    $('.dashboard-change-form.seller').show();
    $('#btn_basic_info').css('color','black');
    $('#btn_seller_info').css('color', '#648efc');
});

// file_upload part
$(document).ready(function(){
    var fileTarget = $('#id_business_license');
    fileTarget.on('change', function(){ // 값이 변경되면
        if(window.FileReader){ // modern browser
            var filename = $(this)[0].files[0].name;
        }
        else { // old IE
            var filename = $(this).val().split('/').pop().split('\\').pop(); // 파일명만 추출
        }
        // 추출한 파일명 삽입
        $(this).siblings('.file_name.business_license').val(filename);
    });

    var fileTarget2 = $('#id_account_copy');
    fileTarget2.on('change', function(){ // 값이 변경되면
        if(window.FileReader){ // modern browser
            var filename2 = $(this)[0].files[0].name;
        }
        else { // old IE
            var filename2 = $(this).val().split('/').pop().split('\\').pop(); // 파일명만 추출
        }
        // 추출한 파일명 삽입
        $(this).siblings('.file_name.account_copy').val(filename2);
    });


    $("#dialog-confirm").dialog({
        resizable: false,
        height:190,
        autoOpen: false,
        width: 330,
        modal: true,
        buttons: [
            {
                text: "예",
                click: function() {
                    $('#go_main').val('True');
                    $('#change_form_user').submit();
                }
            },
            {
                text: "아니오",
                click: function() {
                    $('#go_main').val('False');
                    $('#change_form_user').submit();
                }
            }
        ]
    });

    $("#dialog-confirm2").dialog({
        resizable: false,
        height:190,
        autoOpen: false,
        width: 330,
        modal: true,
        buttons: [
            {
                text: "예",
                click: function() {
                    $('#go_main2').val('True');
                    $('#change_form_seller').submit();
                }
            },
            {
                text: "아니오",
                click: function() {
                    $('#go_main2').val('False');
                    $('#change_form_seller').submit();
                }
            }
        ]
    });

    $('.change_button_seller').on('click', function() {
        $("#dialog-confirm2").dialog('open');
    });

});


$(document).ready(function() {
    $('.seller_form_input.type input').on('change', function(){
        show_by_seller_type();
    });
});

function show_by_seller_type(){
    if($('#id_type_0').is(":checked")){
        $('.seller_form_content.company_name').hide();
        $('.seller_form_content.representative_name').hide();
        $('.seller_form_content.corporate_number').hide();
        $('.seller_form_content.business_field').hide();
        $('.seller_form_content.company_type').hide();
        $('.seller_form_content.business_license').hide();
        $('.seller_form_content.account_copy').hide();
    }else{
        $('.seller_form_content').show();
    }
}

/* graph part */
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
    $('.graph-part.ads span:nth-child(2)').css('width', calculated_ads_normal + '%');
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