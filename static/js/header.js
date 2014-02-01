initHeader = function(){
	document.getElementById('searchJobIcon').onclick = function(){
		alert('here1')
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
			// alert('hereeeeeeeee')
			// console.log($('#searchType').attr('class'))
			if($('#searchType').attr('class').indexOf('disabled') < 0){
				if($('#searchType').attr('name') == '1'){
					// $(this).text('فرصت شغلی');
					$('#searchType').attr('name', '0');
				}
				else{
					// $(this).text('کارجو');	
					$('#searchType').attr('name', '1');
				}
			}
			// console.log($('#searchType').attr('name'))
			// alert($('#searchType').attr('name'))
		}
	});

	// $('#search-type').on('click', function(){
	// 	if($(this).attr('class').indexOf('disabled') < 0){
	// 		if($(this).attr('name') == '1'){
	// 			$(this).text('فرصت شغلی');
	// 			$(this).attr('name', '0');
	// 		}
	// 		else{
	// 			$(this).text('کارجو');	
	// 			$(this).attr('name', '1');
	// 		}
	// 	}
	// });
}


$(document).ready(function(){
	initHeader();
	// alert($('#searchType').val())
});