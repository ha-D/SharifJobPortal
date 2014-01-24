var search = {query : ''}
init = function(){
	$('.icon.delete').on('click', function(){
		$(this).parent().remove();
	});

	$('.opp-more').on('click', function(){
		
	});
	
	$('#tag-search-input input').on('keyup', function(){
		query = $(this).val();
		$.ajax({
			url : '/search/skill/?q=' + query,
			type : 'get',
			dataType : 'html',
			success: function(data, status, xhr){
				newDiv = $(data);
				// console.log(data);
				newDiv = $(newDiv.find('#tag-search-list')[0]);
				// console.log(newDiv.length);
				$('#tag-search-list').remove();
				$('#side-segment').append(newDiv);
				$('.tag-link').on('click', function(){
					newSkill = $(this).text().trim();
					// $(this).remove()
					tags = $('.skill-tag');
					var found = false;
					for(var i = 0 ; i < tags.length ; i++){
						if(newSkill === $(tags[i]).text().trim()){
							found = true;
							break;
						}
					}
					if(!found){
						$('#tag-divider').before('<div class="ui label skill-tag"><i class="delete icon"></i>' + newSkill + '</div>');
						$('.delete.icon').on('click', function(){
							$(this).parent().remove();
						});
					}
				});

			},
			error: function(xhr, status, error){

			},
		});
	});

	
	document.getElementById('searchJobIcon').onclick = function(){
		query = $('#searchJob').val().trim();	
		
		if($('#search-type').attr('name') == '0'){
			skillOb = $('.skill-tag');
			skills = new Array();
			for(var i = 0 ; i < skillOb.length ; i++){
				skills[i] = $(skillOb[i]).text().trim();
			}
			skillString = JSON.stringify(skills);
			window.location.href = '/search?q='+query + '&sk=' + skillString;
		}
		else{
			searchAjax(query, 1)
		}
	};

	$('.pagination-item').on('click', function(e){
		curPage = parseInt($('.pagination-item.active').text().trim());
		reqPage = parseInt($(this).text().trim());
		if(!isNaN(reqPage) && curPage !== reqPage){
			searchAjax(search['query'], reqPage)
		}

	});

	
	$('.left.arrow').parent().on('click', function(e){
		curPage = parseInt($('.pagination-item.active').text().trim());
		searchAjax(search['query'], curPage-1);
	});

	$('.right.arrow').parent().on('click', function(e){
		curPage = parseInt($('.pagination-item.active').text().trim());
		searchAjax(search['query'], curPage+1);
	});
}

searchAjax = function(query, page){
	if(query.length >= 0){
		skillOb = $('.skill-tag');
		skills = new Array();
		for(var i = 0 ; i < skillOb.length ; i++){
			skills[i] = $(skillOb[i]).text().trim();
		}
		skillString = JSON.stringify(skills);
		console.log(skillString);
		$.ajax({
			url: '/search/user?ajax&q=' + query + '&sk=' + skillString + '&page=' + page,
			type : 'get',
			dataType : 'html',
			success : function(data, status, xhr){
				newDiv = $(data);
				console.log(data)
				newDiv = $(newDiv.find('#search-results')[0]);
				$('#search-results').remove();
				$('#main').append(newDiv);
				// console.log($('#main').html())
				init();
				search['query'] = query;
				window.scrollTo(0);
			},
			error : function(xhr, status, error){

			},
		});
	}
}



window.onload = function(){
		init();
};	