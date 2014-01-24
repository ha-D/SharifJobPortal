initHeader = function(){
	document.getElementById('searchJobIcon').onclick = function(){
		query = $('#searchJob').val().trim();
		if(query.length > 0){
			window.location.href = '/search/?q=' + query;
		}
	};
}

$(document).ready(function(){
	initHeader();
});