var statuses = {};

$(function () {
    // 전체 목록에서 각 상태 별로 숫자세기..
    $('.order-list-table tr[data-status]').each(function(i, el) {
        var status = $(el).data('status');
        if (statuses.hasOwnProperty(status))
            statuses[status] += 1;
        else
            statuses[status] = 1;
    });

    // 상단 상태버튼들 안의 괄호에 숫자 채워넣기..
    $('.order-list-nav li[data-status]').each(function(i, el) {
        var status = $(el).data('status');
        if (statuses.hasOwnProperty(status))
            $(this).children('span.status-count').html('' + statuses[status]);
        else
            $(this).children('span.status-count').html('0');
    });

    // 상단 상태버튼을 눌렀을 때의 처리..
    $('.order-list-nav ul li').click(function() {
        $('.order-list-nav ul li').removeClass('active');
        $(this).addClass('active');

        if ($(this).data('status')) {
            $('.order-list-table tbody tr').hide();
            $('.order-list-table tbody tr[data-status="{}"]'.format($(this).data('status'))).show();
        } else {
            $('.order-list-table tbody tr').show();
        }
    });

    // 전체 선택 버튼을 눌렀을 경우..
    $('.order-list-table th input[type="checkbox"]').change(function() {
        $('.order-list-table td input[type="checkbox"]').prop('checked', this.checked);
    });
});
