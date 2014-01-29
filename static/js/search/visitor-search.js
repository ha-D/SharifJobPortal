search = {}
search['query'] = ''
FADE_SPEED = 400
init = function(){
	$('.icon.delete').on('click', function(){
		$(this).parent().remove();
	});

	$('.opp-more').on('click', function(){
		info = $($(this).parent().siblings('ul')[0]).children()
		// console.log(info.length)
		textInfo = new Array()
		for(var i = 0 ; i < info.length ; i++){
			textInfo[i] = $(info[i]).html();
			// console.log(textInfo[i]);
		}
		name = $(this).parent().parent().find('.opp-header').text();
		$('#opName').html(name);
		opList = $('#opList').children();
		sexInt = parseInt(textInfo[0]);
		switch(sexInt){
			case 0:
				$(opList[0]).html('<i class="male icon"></i>مرد');
				break;
			case 1:
				$(opList[0]).html('<i class="female icon"></i>زن');
				break;
			case 2:
				$(opList[0]).html('<i class="male icon" id="sex-one"></i><i class="female icon"></i>مرد-زن');
				break;
		}
		for(var i = 1 ; i < 4 ; i++){
			content = $($(opList[i]).children('i')[0]).attr('class');
			$(opList[i]).html($('<i>').attr('class', content));
			$(opList[i]).append(textInfo[i]);
		}
		companyList = $('#companyList').children();
		for(var i = 0 ; i < 6 ; i++){
			content = $($(companyList[i]).children('i')[0]).attr('class');
			$(companyList[i]).html($('<i>').attr('class', content));
			if(i == 4){
				$(companyList[i]).append($('<a>').attr('href', textInfo[4 + i]).html(textInfo[4 + i]));
			}
			else{
				$(companyList[i]).append(textInfo[i + 4]);
			}
		}
		$('#companyImage img').attr('src', textInfo[10]);
		skills = textInfo[13].split(' ');
		console.log(skills.join())
		$(companyList[6]).html($('<i>').attr('class', 'info icon'))
		$(companyList[6]).append(skills.join('، '))
		$('.ui.modal').modal('show');
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
		searchAjax(query, 1)
		
	};

	document.getElementById('searchForm').onsubmit = function(){
		query = $('#searchJob').val().trim();
		searchAjax(query, 1)
		return false;	
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
				url: '/search/?ajax&q=' + query + '&sk=' + skillString + '&page=' + page,
				type : 'get',
				dataType : 'html',
				success : function(data, status, xhr){
					newDiv = $(data);
					newDiv = $(newDiv.find('#search-results')[0]);
					$('#search-results').remove();
					$('#main').append(newDiv);
					init();
					$('.ui.rating').rating('disable');
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
	$('.ui.rating').rating('disable');
	
};