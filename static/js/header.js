initHeader = function(){
	document.getElementById('searchJobIcon').onclick = function(){
		query = $('#searchJob').val().trim();
		if(query.length > 0){
			if($('#searchType').attr('name') == '0'){
				// window.location.href = '/search/op?q=' + query;
				$('#headerForm').attr('action', '/search/op');
				$($('#headerForm').children()[0]).val(query);
				$('#headerForm').submit();
			}
			else{
				$('#headerForm').attr('action', '/search/user');
				$($('#headerForm').children()[0]).val(query);
				$('#headerForm').submit();
			}
		}
	};

	document.getElementById('searchForm').onsubmit = function(){
		query = $('#searchJob').val().trim();
		if(query.length > 0){
			if($('#searchType').attr('name') == '0'){
				$('#headerForm').attr('action', '/search/op');
				$($('#headerForm').children()[0]).val(query);
				$('#headerForm').submit();
			}
			else{
				$('#headerForm').attr('action', '/search/user');
				$($('#headerForm').children()[0]).val(query);
				$('#headerForm').submit();
			}
		}
		return false;
	};

	$('#searchType').checkbox({
		onChange : function(){
			if($('#searchType').attr('class').indexOf('disabled') < 0){
				if($('#searchType').attr('name') == '1'){
					$('#searchType').attr('name', '0');
				}
				else{
					$('#searchType').attr('name', '1');
				}
			}
		}
	});

    if ($('#searchType').attr('class').indexOf('disabled') < 0
        && $('#searchType').attr('name') == '0' ){
        $('#searchTypeDiv').checkbox('enable');
    }
};


$(document).ready(function(){
	initHeader();
	// alert($('#searchType').val())
});