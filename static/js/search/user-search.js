var search = {query : ''}
search['inRating'] = false;
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
		// console.log(skills.join())
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
		searchButton();
	};

	document.getElementById('searchForm').onsubmit = function(){
		// alert('here1')
		searchButton();
		return false
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

searchButton = function(){
	query = $('#searchJob').val().trim();	
		if($('#searchType').attr('name') == '1'){
			skillOb = $('.skill-tag');
			skills = new Array();
			for(var i = 0 ; i < skillOb.length ; i++){
				skills[i] = $(skillOb[i]).text().trim();
			}
			skillString = JSON.stringify(skills);
			// var x = '/search/user?q='+query + '&sk=' + skillString
			// window.location.href = x;
			// console.log(skillString)
			// console.log(query)
			// alert('done')
			$($('#postForm').children()[0]).val(query)
			$($('#postForm').children()[1]).val(skillString)
			$('#postForm').submit()
		}
		else{
			// alert($('#searchType').attr('name'))
			// alert('opp1')
			searchAjax(query, 1)
		}
}



searchAjax = function(query, page){
	if(query.length >= 0){
		skillOb = $('.skill-tag');
		skills = new Array();
		for(var i = 0 ; i < skillOb.length ; i++){
			skills[i] = $(skillOb[i]).text().trim();
		}
		skillString = JSON.stringify(skills);
		// console.log(skillString);
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
				initRating();
				search['query'] = query;
				window.scrollTo(0);
			},
			error : function(xhr, status, error){

			},
		});
	}
}


initRating = function(){
	$('.ui.rating.opp-rating').rating({onRate : function(e){
		// curStar = e
		// console.log(curStar)
		// console.log('eee is', e)
		curRate1 = $(this).rating('get rating');
		pholder1 = $(this).prev()
		// if($(this).attr('class').indexOf('opp-rating') >= 0){
		opid = $($($(this).parent().siblings('ul')[0]).children()[11]).html();
		$.ajax({
			url : '/search/rate/?op=' + parseInt(opid) + '&rate=' + curRate1,
			type : 'get',
			dataType : 'json',
			success: function(data, status, xhr){
				// alert('doing ajax')
				if(data['result'] == 1){
					pholder1.html('امتیاز کنونی : ' + data['rate']);
				}
			},

			error: function(xhr, status, error){

			},
		});
		// }
	}} ) ;

	$('.user-rating').rating({onRate : function(e){
		if(!search['inRating']){
			curRate = $(this).rating('get rating');
			// alert($(this).attr('id'))
			pholder = $(this).prev()
			search['inRating'] = true;
			empid = $($($(this).parent().parent().parent().siblings('ul')[0]).children()[12]).html()
			$.ajax({
				url : '/search/rate/?emp=' + parseInt(empid) + '&rate=' + curRate,
				type : 'get',
				dataType : 'json',
				success: function(data, status, xhr){
					// alert('doing ajax 2')
					// console.log('staaars', data['rate'])
					if(data['result'] == 1){
						allEmps = $('.compId')

						for(var i = 0 ; i < allEmps.length ; i++){
							if(parseInt($(allEmps[i]).text()) == parseInt(empid)){
								ratingOb = $($(allEmps[i]).parent().parent().find('.small.rating')[0])
								
								ratingOb.rating('set rating', parseInt(data['rate']));
								ratingOb.prev().html('امتیاز کنونی: ' + data['rate']);
							}
						}
						pholder.html('امتیاز کنونی: ' + data['rate']);
						search['inRating'] = false;
					}
					else{
						search['inRating'] = false;
					}
				},

			error: function(xhr, status, error){
				// alert('erooororor')
				search['inRating'] = false;
				},
			});
		}
	}});
}

window.onload = function(){
		init();
		initRating();
		search['query'] = $('#query').html();
		$('#searchJob').val(search['query']);
		// $('.small.rating').rating('set rating', 1)
};	