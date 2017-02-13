$(document).ready(function () {
	$('.contact').hover(function () {
		$('.contact .contact-drop-down').stop(true, false, true).slideToggle(300);
	});
	var elementPosition = $('.contact').offset();
	var temp =0;
	temp = $(window).scrollTop() + $(window).height() - $(document).height() + 124;
	if($(window).scrollTop() + $(window).height() > $(document).height() - 124){
		$('.contact').css({'position':'fixed','bottom':temp, 'left':'87%', 'margin-bottom':'0'});
	} else {
		$('.contact').css({'position':'fixed','bottom':'0', 'left':'87%', 'margin-bottom':'1%'});
	}
	$(window).scroll(function(){
		temp = $(window).scrollTop() + $(window).height() - $(document).height() + 124;
		if($(window).scrollTop() + $(window).height() > $(document).height() - 124){
			$('.contact').css({'position':'fixed','bottom':temp, 'left':'87%', 'margin-bottom':'0'});
		} else {
			$('.contact').css({'position':'fixed','bottom':'0', 'left':'87%', 'margin-bottom':'1%'});
		}
	});
});
