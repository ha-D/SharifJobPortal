portal = {};

function relaxUI(){
	// $("body").on('onload', ".ui.checkbox", function(){
	// 	$(this).checkbox();
	// 	console.log(this)
	// })

	// $("body").on('load', ".ui.dropdown", function(){
	// 	$(this).checkbox();
	// })


    $('.ui.checkbox').checkbox();
    // $('.ui.radio.checkbox').checkbox();
    $('.ui.dropdown').dropdown();
    $('.submitButton').click(function(event){
        $(event.target).closest("form").submit();
    });
}

function getParam ( sname )
{
	var params = location.search.substr(location.search.indexOf("?")+1);
	var sval = "";
	params = params.split("&");
	for (var i=0; i<params.length; i++) {
		temp = params[i].split("=");
		if ( [temp[0]] == sname ) { 
			sval = temp[1]; 
		}
	}
	return sval;
}

portal.showConfirmDialog = function(message, yesCallback, noCallback){
	$('#confirmbox .content').html(message);
	$('#confirmbox').modal('show')
	$('#confirmbox .yes.button').unbind('click');
	$('#confirmbox .no.button').unbind('click');
	if(typeof(yesCallback) == 'function')
		$('#confirmbox .yes.button').click(yesCallback);
	if(typeof(noCallback) == 'function')
		$('#confirmbox .no.button').click(noCallback);
	$('#confirmbox .button').click(function(){
		$("#confirmbox").modal("hide");
	});
}



function link(href){
    window.location.href = href;
}


portal.zComment = function(options){
	var zSeg = $(this);

	if(options === undefined)
		options =  {}
	
	function addComment(comment){
		var comDiv = zSeg.find('.ui.comments')
		var comm = $("<div>").addClass('comment');
		// comm.append($("<a>").addClass('avatar').append($("<img>").attr('src', comment.image)));

		var content = $("<div>").addClass("content");
		content.append($("<a>").addClass("author").attr('href', comment.author_url)
			.text(comment.author));
		content.append($("<div>").addClass("metadata")
			.append($("<span>").addClass("date").text(comment.date)));
		content.append($("<div>").addClass("text").text(comment.content));

		comm.append(content);
		comDiv.append(comm);
	}

	function addComments(comments, page, pageCount){
		console.log(comments);
		var comDiv = zSeg.find('.ui.comments')
		comDiv.html('');
		for(var i = 0; i < comments.length; i++){
			addComment(comments[i]);
		}

		var pagesDiv = zSeg.find('.pagination .items');
		pagesDiv.html('');
		for(var i = 1; i <= pageCount; i++){
			var a = $("<a>").addClass('item');
			if(i == page)
				a.addClass('active');
			a.attr('data-page', i);
			a.html(i);
			pagesDiv.append(a);
		}

		if(comments.length > 0){
			zSeg.find('.right .pagination').show();
			zSeg.find('.right .columnholder').hide();
		}else{
			zSeg.find('.right .columnholder').show();
		}
	}

	function loadPage(page){
		$.ajax({
			url: zSeg.options.url,
			type: 'post',
			data: { action: 'list', page: page, page_size: zSeg.options.pageSize },
			success: function(data){
				if(data.result == 'success'){
					addComments(data.comments, data.page, data.pageCount);
					zSeg.currentPage = data.page;
				}
			}
		})
	}

	if(typeof(options) == 'object'){
		/* Initial Values */
		options.title = options.title || 'نظرات';
		options.pageSize = options.pageSize || 5;
		if(!options.url){
			throw "Must give a url for zComments";
		}
		if(options.pagination === undefined)
			options.pagination = true;
		if(options.addForm === undefined)
			options.addForm = true;

		/* Initialize */
		if(!zSeg.hasClass("commentseg"))
			zSeg.addClass('commentseg');
		zSeg.html('');
		zSeg.options = options;


		/* Initialize Html */
		zSeg.append($("<h2>").addClass("ui header").
			append($("<i>").addClass("icon comment")).append(options.title));

		var pagination = $("<div>").addClass("ui pagination menu");
		pagination.append($("<a>").addClass("icon next item").append($("<i>").addClass("icon right arrow")));
		pagination.append($("<div>").addClass("items"));
		pagination.append($("<a>").addClass("icon previous item").append($("<i>").addClass("icon left arrow")));

		var holder = $("<div>").addClass("columnholder");
		var right = $("<div>").addClass("right");
		right.append($("<div>").addClass("ui comments"));
		right.append(holder);
		if(options.pagination)
			right.append(pagination);

		var left = $("<div>").addClass("left");
		var form = $("<form>").addClass("ui reply form");
		form.append($("<div>").addClass("field").append($("<textarea>").addClass("add text")));
		form.append($("<div>").addClass("ui fluid green labeled submit icon button")
			.append($("<i>").addClass("icon edit")).append("ثبت نظر"));
		if(options.addForm)
			left.append(form);

		holder.show();
		pagination.hide();
		zSeg.append(right).append(left);



		/* Event Handlers */

		zSeg.on('click', '.pagination .items .item', function(){
			var page = $(this).attr('data-page');
			loadPage(page);
		})

		zSeg.on('click', '.pagination .previous.item', function(){
			var page = zSeg.currentPage + 1;
			loadPage(page);
			console.log($(this).parent());	
			$(this).removeClass('active');
		})

		zSeg.on('click', '.pagination .next.item', function(){
			var page = zSeg.currentPage - 1;
			loadPage(page);
			$(this).removeClass('active');
		})

		zSeg.find('.submit.button').click(function(){
			var comment = zSeg.find('textarea.add.text').val();
			$.ajax({
				url: zSeg.options.url,
				type: 'post',
				data: { action: 'add', comment: comment, page_size: zSeg.options.pageSize},
				success: function(data){
					if(data.result == 'success'){
						addComments(data.comments);
					}else{
						console.log('Error');
						console.log(data);
					}
				}
			})
		})

		loadPage(1);

	}else if(typeof(options) == 'string'){

	}

}

$(document).ready(function(){
	relaxUI();
	$(".footer").load('/footer');
	$('#confirmbox').modal()


	$.fn.zComment = portal.zComment;
});

