$(function () {
    var price_ = $('.price');
    var first_option = $('#id_variation_set-0-title');

    $('.panel-body').css('height', '400px');

    $('.post_image').on('click', function () {
        $('#id_image').trigger('click');
    });

    $('#id_image').change(function () {
        readImage(this);
    });

    first_option.val('기본가');
    first_option.on('click', function () {
        $('#id_variation_set-0-price').focus();
        alert('기본가 옵션명은 변경할 수 없습니다.');
    });
    $('#id_variation_set-0-is_default').attr('checked', 'true');

    var subject_all_html = '<label for="id_all"><input id="id_all" name="tag" type="checkbox" value="">전체</label>';

    price_.on('click', '.plus', function () {
        var nxt_num = $('.price_field').length;
        $('#id_variation_set-TOTAL_FORMS').val(nxt_num + 1);

        var price_html = '<div class="price_field">' +
            '<input class="variation_title" id="id_variation_set-' + nxt_num + '-title" maxlength="120" name="variation_set-' + nxt_num + '-title" placeholder="옵션 이름" type="text">' +
            '<input class="variation_price" id="id_variation_set-' + nxt_num + '-price" name="variation_set-' + nxt_num + '-price" type="text" value="0">' +
            '<span class="unit">원</span>' +
            '<div class="options minus">' +
            '<i class="fa fa-minus" aria-hidden="true"></i>' +
            '</div>' +
            '<input id="id_variation_set-' + nxt_num + '-is_default" name="variation_set-' + nxt_num + '-is_default" type="checkbox">' +
            '<input id="id_variation_set-' + nxt_num + '-id" name="variation_set-' + nxt_num + '-id" type="hidden">' +
            '<input id="id_variation_set-' + nxt_num + '-product" name="variation_set-' + nxt_num + '-product" type="hidden">' +
            '</div>';

        $(price_html).insertAfter($('.price .form-area .price_field').last());
    });

    price_.on('click', '.minus', function () {
        $(this).parent().remove();
        var price_field = $('.price_field');

        var total_num = price_field.length;
        $('#id_variation_set-TOTAL_FORMS').val(total_num);
        price_field.each(function (index) {
            $(this).find('input').each(function () {
                var ele_id = $(this).attr('id').split('-');
                if (ele_id.length == 3) {
                    var new_id = ele_id[0] + '-' + index.toString() + '-' + ele_id[2];
                    $(this).attr('id', new_id);
                }

                var ele_name = $(this).attr('name').split('-');
                if (ele_name.length == 3) {
                    var new_name = ele_id[0] + '-' + index.toString() + '-' + ele_id[2];
                    $(this).attr('name', new_name);
                }
            });
        });
    });

    $('.buttons .start').on('click', function () {
        var step = $.trim($('.step_num.active .title').text());
        $('.step_num').removeClass('active');

        if (step == 'STEP1') {
            checkstep1();
        } else if (step == 'STEP2') {
            checkstep2();
        }
    });

    $('.form-right').on('click', '.add_url', function () {
        var url_html = '<br/><div class="form-url-input add-url-input">' +
            '<input id="id_url" name="url" type="text">' +
            '<div class="button minus">-</div>' +
            '<input type="checkbox" id="is_active" checked><label for="is_active">비공개</label>' +
            '</div>';

        $(url_html).insertAfter($('.form-url-input').last());
    });

    $('.form-right').on('click', '.minus', function () {
        $(this).parent().prev().remove();
        $(this).parent().remove();
    });

});

function readImage(input) {
    if (input.files && input.files[0]) {
        var image = new FileReader();

        image.onload = function (e) {
            $('#post_image').attr('src', e.target.result);
        };

        image.readAsDataURL(input.files[0])
        $('#default_image').hide();
        $('.post_image h2').hide();
    }
}

function checkstep1() {
    $('.step_num#step1_').addClass('active');
    // if (!$('#id_title').val()) {
    //     alert('제목을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_title').offset().top - 60
    //     }, 300);
    //     $('#id_title').focus();
    // } else if (!$('#id_url').val()) {
    //     alert('SNS 주소를 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_url').offset().top - 60
    //     }, 300);
    //     $('#id_url').focus();
    // } else if (!$('#id_influence').val()) {
    //     alert('SNS 영향력을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_influence').offset().top - 60
    //     }, 300);
    //     $('#id_influence').focus();
    // } else if (!$('#id_image').val()) {
    //     alert('메인 이미지를 등록해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#post_image').offset().top - 60
    //     }, 300);
    // } else if (!$('input[name="type"]').is(":checked")) {
    //     alert('광고 가능한 SNS 종류를 선택해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('.filter').offset().top - 60
    //     }, 300);
    // } else if (!$('input[name="tag"]').is(":checked")) {
    //     alert('주로 다루는 주제를 선택해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('.filter').offset().top - 60
    //     }, 300);
    // } else if (!$('input[name="target"]').is(":checked")) {
    //     alert('주로 참여하는 타겟층을 선택해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('.filter').offset().top - 60
    //     }, 300);
    // } else {
        $('.step1').hide().removeClass('active');
        $('.step2').show().addClass('active');
        $('.step_num#step2_').addClass('active');
        $('.step_num#step1_').removeClass('active');
    // }
}

function checkstep2() {
    $('.step_num#step2_').addClass('active');

    // if (!$('#id_required').val()) {
    //     alert('유의사항을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_required').offset().top - 60
    //     }, 300);
    //     $('#id_required').focus();
    // } else if (!$('#id_command').val()) {
    //     alert('지시사항을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_command').offset().top - 60
    //     }, 300);
    //     $('#id_command').focus();
    // } else if (!$('#id_refund').val()) {
    //     alert('환불 규정을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_refund').offset().top - 60
    //     }, 300);
    //     $('#id_refund').focus();
    // } else if (!$('#id_description').val()) {
    //     alert('상품 상세 내용을 입력해주세요.');
    //     $('html, body').animate({
    //         scrollTop: $('#id_description').offset().top - 60
    //     }, 300);
    //     $('#id_description').focus();
    // } else {
        $('.step2').hide().removeClass('active');
        $('.step3').show().addClass('active');
        $('.step_num#step3_').addClass('active');
        $('.step_num#step2_').removeClass('active');
        $('.buttons .final').show();
        $('.buttons .start').hide();
    // }
}