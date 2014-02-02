$.fn.zedit = function(){
	var zedit = $(this);

	function addItem(options){
		var itemDiv =  $("<div>").addClass("zedit item").addClass(options.page_id.toString());
		itemDiv.attr('data-item-id', options.page_id);
		
		var titleDiv = $("<div>").addClass("zedit title");
		titleDiv.append($("<h4>").append($("<i>").addClass("icon remove")).append(options.title));
		itemDiv.append(titleDiv);

		var markup = $("<textarea>").addClass("zedit markup");
		if(options.content){
			markup.val(options.content);
		}
		
		itemDiv.append(markup);
		zedit.find('.zedit.items').append(itemDiv);

		var buttonsDiv = $("<div>").addClass("zedit buttons");
		buttonsDiv.append($("<div>").addClass("zedit ui tiny green save button").html("دخیره تغییرات"));
		buttonsDiv.append($("<div>").addClass("zedit ui tiny blue preview button").html("نمایش"));
		buttonsDiv.append($("<div>").addClass("zedit status"));

		markup.markItUp(mySettings);
		// x = itemDiv;
		itemDiv.find('.markItUpButton a').html("");
		itemDiv.find('.markItUpFooter').append(buttonsDiv);
	}

	function removeItem(item_id){
		zedit.children('zedit item ' + item_id).remove();
	}

	if(typeof(arguments[0]) == 'string'){
		var com = arguments[0];
		if(com == 'add item'){
			var options = arguments[1];
			addItem(options);
		}else if(comm == 'remove item'){
			removeItem(arguments[1]);
		}

	}else if(typeof(arguments[0]) == 'object'){
		var options = arguments[0];
		zedit.options = options;
		
		if(zedit.options.url === undefined){
			console.log("zEdit error: no url given");
			return;
		}

		/* Initializing new zEdit */

		zedit.html('');
		zedit.append($('<div>').addClass('zedit items'));

		if(zedit.options.showAddForm !== false){
			var addDiv = $('<div>').addClass('zedit add');
			addDiv.append($('<div>').addClass('message').html('برای اضافه کردن صفحه جدید نام آن را وارد کنید'));

			var input = $('<input>').attr('type', 'text').attr('placeholder', 'نام صفحه جدید');
			var button = $('<div>').addClass('ui small blue button').html('اضافه');
			addDiv.append($('<div>').addClass('ui  input').append(input)).append(button);

			zedit.append(addDiv);
		}


		/* Initialize modal */

		var modal = $("<div>").addClass('ui modal zedit');
		var modalHeader = $("<div>").addClass("header");
		var modalContent = $("<div>").addClass("content");
		modal.append($("<i>").addClass("close icon"));
		// modal.append(modalHeader);
		modal.append(modalContent);
		$('body').append(modal);
		modal.modal();


		/* Add items */

		if(options.items){
			for(var i = 0; i < options.items.length; i++){
				addItem(options.items[i]);
			}
		}


		/* Load data */

		$.ajax({
			url: zedit.options.url,
			type: 'post',
			dataType: 'json',
			data: {action:'list'},
			success: function(data){
				if(data.result == 'success'){
					for(var i = 0; i < data.pages.length; i++){
						addItem(data.pages[i]);
					}							
				}else{
					console.log(data)
				}
			},
			error: function(data){
				throw data;
			}
		})

		/* Event handlers */

		function successStatus(item, message){
			item.find('.zedit.status').removeClass('error').addClass('success').html(message);
		}

		function errorStatus(item, message){
			item.find('.zedit.status').addClass('error').removeClass('success').html(message);
		}

		zedit.on('click', '.save.button', function(){
			var item = $(this).parents('.zedit.item');
			var item_id = item.attr('data-item-id');
			var content = item.find('textarea').val()
			$.ajax({
				url: zedit.options.url,
				type: 'post',
				dataType: 'json',
				data: {action:'save', page_id: item_id, content: content},
				success: function(data){
					if(data.result == 'success')
						successStatus(item,'تغییرات با موفقیت ثبت شد')
					else
						errorStatus(item,'در ذخیره تغییرات خطا رخ داده است');
					
				},
				error: function(data){
					errorStatus(item,'در ذخیره تغییرات خطا رخ داده است');
				}
			})
		})

		zedit.on('click', '.remove.icon', function(){
			var item = $(this).parents('.zedit.item');
			var item_id = item.attr('data-item-id');
			var title = item.find('.title').text();
			portal.showConfirmDialog('آیا مایل به حذف صفحه ' + title + 'هستید؟', function(){
				$.ajax({
					url: zedit.options.url,
					type: 'post',
					dataType: 'json',
					data: {action:'remove', page_id: item_id},
					success: function(data){
						if(data.result == 'success'){
							successStatus(item,'تغییرات با موفقیت ثبت شد')
							zedit.find('.zedit.item.' + item_id).remove();
						}else
							errorStatus(item,'در ذخیره تغییرات خطا رخ داده است');
						
					},
					error: function(data){
						errorStatus(item,'در ذخیره تغییرات خطا رخ داده است');
					}
				})
			});
		})

		zedit.on('click', '.preview.button', function(){
			var preview_url = '/zedit/preview/';
			if(options.preview_url !== undefined){
				preview_url = options.preview_url;
			}
			var item = $(this).parents('.zedit.item');
			var item_id = item.attr('data-item-id');
			$.ajax({
				url: preview_url,
				type: 'post',
				dataType: 'json',
				data: {content: item.find('.markup').val()},
				success: function(data){
					if(data.result == 'success'){
						successStatus(item, '');

						modalHeader.html(item.find('.zedit.title h4').text());
						modalContent.html(data.content);
						modal.modal('show')
					}else{
						errorStatus(item, 'در نمایش صفحه خطا رخ داده است');
					}
				},
				error: function(data){
					errorStatus(item, 'در نمایش صفحه خطا رخ داده است');
				}
			})
		})

		zedit.on('click', '.add .button', function(){
			var name = zedit.find('.add input').val();
			if(name){
				$.ajax({
					url: zedit.options.url,
					type: 'post',
					dataType: 'json',
					data: {action: 'add', title: name},
					success: function(data){
						if(data.result == 'success'){
							addItem(data.page);
							zedit.find('.add input').val('');	
						}else{
							throw data;
						}
					}
				})
			}
		})	
	}


}
