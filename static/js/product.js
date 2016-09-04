$(function () {
    var price_ = $('.price');
    var variation_total = $('#id_variation_set-TOTAL_FORMS');

    // set variation total num is 1
    variation_total.val(1);


    // set summer-note initial height
    $('.panel-body').css('height', '400px');

    // trigger post image
    $('.post_image').on('click', function () {
        $('#id_image').trigger('click');
    });

    // image input file is change
    $('#id_image').change(function () {
        readImage(this);
    });

    //checking variation first item is filled
    $('#id_variation_set-1-price').blur(function () {
       if(!$.trim(this.value).length) {
           variation_total.val(2);
       }
    });

    $('#id_variation_set-1-title').blur(function () {
       if(!$.trim(this.value).length) {
           variation_total.val(2);
       }
    });

    $('#id_variation_set-1-day').blur(function () {
       if(!$.trim(this.value).length) {
           variation_total.val(2);
       }
    });

    $('#id_variation_set-0-is_default').attr('checked', 'true');

    $('#id_variation_set-0-price').attr('placehoder', '10,000원 이상, 1,000원 단위로 가능');

    var subject_all_html = '<label for="id_all"><input id="id_all" name="tag" type="checkbox" value="">전체</label>';

    price_.on('click', '.plus', function () {
        var nxt_num = $('.price-option-area').length + 2;
        $('#id_variation_set-TOTAL_FORMS').val(nxt_num);

        var price_html = '<div class="price-option-area">' +
            '<div class="form-input">' +
            '<input class="variation_price" id="id_variation_set-' + nxt_num + '-price"' +
            'name="variation_set-' + nxt_num + '-price" placeholder="옵션의 추가 비용"> ' +
            '<label>원 추가시</label>' +
            '</div>' +
            '<div class="form-input">' +
            '<input class="variation_title" id="id_variation_set-' + nxt_num + '-title"' +
            'name="variation_set-' + nxt_num + '-title" placeholder="추가 비용을 지불 시 제공하는 상품 내용">' +
            '</div>' +
            '<div class="form-input">' +
            '<input class="variation_day" id="id_variation_set-' +  nxt_num + '-day"' +
            'name="variation_set-' + nxt_num + '-day" placeholder="옵션 구매 시 추가 일수">' +
            '<label>일 추가</label>' +
            '</div>' +
            '<div class="options minus">' +
            '<i class="fa fa-minus" aria-hidden="true"></i>' +
            '</div>' +
            '</div>';

        $(price_html).insertAfter($('.price .form-area .price-option-area').last());
    });

    price_.on('click', '.minus', function () {
        $(this).parent().remove();
        var price_field = $('.price-option-area');

        var total_num = price_field.length;
        $('#id_variation_set-TOTAL_FORMS').val(total_num + 1);
        price_field.each(function (index) {
            $(this).find('input').each(function () {
                var ele_id = $(this).attr('id').split('-');
                if (ele_id.length == 3) {
                    var new_id = ele_id[0] + '-' + (index + 1).toString() + '-' + ele_id[2];
                    $(this).attr('id', new_id);
                }

                var ele_name = $(this).attr('name').split('-');
                if (ele_name.length == 3) {
                    var new_name = ele_id[0] + '-' + (index + 1).toString() + '-' + ele_id[2];
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
            '</div>';

        $(url_html).insertAfter($('.form-url-input').last());
    });

    $('.form-right').on('click', '.minus', function () {
        $(this).parent().prev().remove();
        $(this).parent().remove();
    });

    $('.step_num').on('click', function () {
        var step = $(this).attr('id');
        $('.step_num').removeClass('active');

        if (step == 'step1_') {
            $('.step_num#step1_').addClass('active');

            $('.step1').show();
            $('.step2').hide();
            $('.step3').hide();

            $('.step_num#step2_').removeClass('active');
            $('.step_num#step3_').removeClass('active');

            $('.buttons .final').hide();
            $('.buttons .start').show();
        } else if (step == 'step2_') {
            checkstep1();
        } else if (step == 'step3_') {
            checkstep2();
        }

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
    if (!$('#id_title').val()) {
        alert('제목을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_title').offset().top - 60
        }, 300);
        $('#id_title').focus();
    } else if (!$('#id_url').val()) {
        alert('SNS 주소를 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_url').offset().top - 60
        }, 300);
        $('#id_url').focus();
    } else if (!$('#id_influence').val()) {
        alert('SNS 영향력을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_influence').offset().top - 60
        }, 300);
        $('#id_influence').focus();
    } else if (!$('#id_image').val()) {
        alert('메인 이미지를 등록해주세요.');
        $('html, body').animate({
            scrollTop: $('#post_image').offset().top - 60
        }, 300);
    } else if (!$('input[name="type"]').is(":checked")) {
        alert('광고 가능한 SNS 종류를 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else if (!$('input[name="tag"]').is(":checked")) {
        alert('주로 다루는 주제를 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else if (!$('input[name="target"]').is(":checked")) {
        alert('주로 참여하는 타겟층을 선택해주세요.');
        $('html, body').animate({
            scrollTop: $('.filter').offset().top - 60
        }, 300);
    } else {
    $('.step1').hide().removeClass('active');
    $('.step2').show().addClass('active');
    $('.step3').hide().removeClass('active');

    $('.step_num#step1_').removeClass('active');
    $('.step_num#step2_').addClass('active');
    $('.step_num#step3_').removeClass('active');

    $('.buttons .final').hide();
    $('.buttons .start').show();
    }
}

function checkstep2() {
    $('.step_num#step2_').addClass('active');

    if (!$('#id_required').val()) {
        alert('유의사항을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_required').offset().top - 60
        }, 300);
        $('#id_required').focus();
    } else if (!$('#id_command').val()) {
        alert('지시사항을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_command').offset().top - 60
        }, 300);
        $('#id_command').focus();
    } else if (!$('#id_refund').val()) {
        alert('환불 규정을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_refund').offset().top - 60
        }, 300);
        $('#id_refund').focus();
    } else if (!$('#id_description').val()) {
        alert('상품 상세 내용을 입력해주세요.');
        $('html, body').animate({
            scrollTop: $('#id_description').offset().top - 60
        }, 300);
        $('#id_description').focus();
    } else {
    $('.step1').hide().removeClass('active');
    $('.step2').hide().removeClass('active');
    $('.step3').show().addClass('active');

    $('.step_num#step1_').removeClass('active');
    $('.step_num#step2_').removeClass('active');
    $('.step_num#step3_').addClass('active');

    $('.buttons .final').show();
    $('.buttons .start').hide();
    }
}