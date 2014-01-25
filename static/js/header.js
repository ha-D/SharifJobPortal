initHeader = function(){
	document.getElementById('searchJobIcon').onclick = function(){
		query = $('#searchJob').val().trim();
		if(query.length > 0){
			if($('#search-type').attr('name') == '0'){
				window.location.href = '/search?q=' + query;
			}
			else{
				window.location.href = '/search/user?q=' + query;
			}
		}
	};

	$('#search-type').on('click', function(){
		if($(this).attr('class').indexOf('disabled') < 0){
			if($(this).attr('name') == '1'){
				$(this).text('فرصت شغلی');
				$(this).attr('name', '0');
			}
			else{
				$(this).text('کارجو');	
				$(this).attr('name', '1');
			}
		}
	});
}

$(document).ready(function(){
	initHeader();
});