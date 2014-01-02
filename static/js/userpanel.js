var userpanel = {}

userpanel.init = function(){
	userpanel.currentPage = 'main';

	Sammy(function() {
		this.get("#inbox/message/:id", function(){
			var id = this.params.id;
			function done(){
				userpanel.loadInbox("message/" + id);
			}

			if(userpanel.currentPage != 'inbox')
				userpanel.loadContent('inbox', done);
			else
				done();
		});

		this.get("#inbox/:page", function(){
			var page = this.params.page;
			function done(){
				userpanel.loadInbox(page);
			}

			if(userpanel.currentPage != 'inbox')
				userpanel.loadContent('inbox', done);
			else
				done();
		});

		this.get('#:page', function() {
			var page = this.params.page;
			if(page == 'inbox'){
				location.hash = 'inbox/list';
				return;
			}
			
			userpanel.loadContent(page);
		});

		this.get('', function() { 
			userpanel.loadContent();
		});
	}).run();
}

userpanel.loadContent = function(content, done){
	if(content == null || content.trim().length == 0)
		content = 'main';

	console.log("Loading  " + content);

	$("#dimmer").dimmer("show");
	setTimeout(function(){
		$.ajax({
			url: "/userpanel/ajax/" + content +"/",
			beforeSend: function(){
				// $("#dimmer").dimmer("show");
			},
			success: function(result){
				$("#content").html(result);
				userpanel.currentPage = content;
				if(done)
					done();
			},
			error: function(){

			},
			complete: function(){
				$("#dimmer").dimmer("hide");
			}
		})		
	}, 200);
}

userpanel.loadInbox = function(content){
	if(content == null || content.trim().length == 0)
		content = 'list';

	console.log("Loading Inbox  " + content);

	$("#inbox-dimmer").dimmer("show");
	setTimeout(function(){
		$.ajax({
			url: "/userpanel/ajax/inbox/" + content +"/",
			beforeSend: function(){
				// $("#dimmer").dimmer("show");
			},
			success: function(result){
				$("#inbox-content").html(result);
			},
			error: function(){

			},
			complete: function(){
				$("#inbox-dimmer").dimmer("hide");
			}
		})		
	}, 200);
}

$(function(){
	// $("#dimmer").dimmer({
	// 	duration: {
	// 		show: 700,
	// 		hide: 1000
	// 	}
	// });

	$("#content").on("click", "#inbox tr", function(){
		var mid = $(this).attr('data-message-id');
		location.hash = "inbox/message/" + mid;
	});

	$("#content").on("click", "#inbox .button.send", function(){
		location.hash = "inbox/send"
	});
  
	userpanel.init();
})