init = function(){
	$('.icon.delete').on('click', function(){
		$(this).parent().remove();
	});

	$('.opp-more').on('click', function(){
		
		$('.ui.modal').modal('show');
	});

}

window.onload = function(){
	$('.ui.rating').rating();
	init();
};	