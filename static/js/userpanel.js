
function loadContent(content){
	if(content == null || content.trim().length == 0)
		content = 'main';

	console.log("Loading  " + content);

	$("#dimmer").dimmer("show");
	setTimeout(function(){
		$.ajax({
			url: "/ajax/userpanel/" + content +"/",
			beforeSend: function(){
				// $("#dimmer").dimmer("show");
			},
			success: function(result){
				$("#content").html(result);
			},
			error: function(){

			},
			complete: function(){
				$("#dimmer").dimmer("hide");
			}
		})		
	}, 200);
}

function loadInbox(content){
	if(content == null || content.trim().length == 0)
		content = 'inbox';

	console.log("Loading Inbox  " + content);

	$("#inbox-dimmer").dimmer("show");
	setTimeout(function(){
		$.ajax({
			url: "/ajax/userpanel/" + content +"/",
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

$(document).ready(function(){
	// $("#dimmer").dimmer({
	// 	duration: {
	// 		show: 700,
	// 		hide: 1000
	// 	}
	// });

	$("#panelmenu .item").click(function(){
		var page = $(this).attr("page");
		history.pushState({type: "panel", state: page}, null, page);
		loadContent(page);
	});

	// var app = Davis(function () {
	// 	this.configure(function () {
	// 	    this.generateRequestOnPageLoad = true
	// 	})
	// 	this.get('/userpanel/', function (req) {
	
	// 	})
	// 	this.get('/userpanel/:name/', function (req) {
	// 		console.log("DAVIS:   " + req.params['name']);
	// 		loadContent(req.params['name']);
	// 	})
	// })
    // app.start()

	window.addEventListener("popstate", function(e) {
		if(e.state == null)
			loadContent();
		else if(e.state.type === "panel"){
			loadContent(e.state.state);
		}else if(e.state.type === "inbox"){
			loadInbox(e.state.state);
		}
		loadContent(e.state);
	});


    $("#content").on("click", "#inbox tr", function(){
    	history.pushState({type: "inbox", state: "samplemail"}, null, "/userpanel/inbox/samplemail");
    	loadInbox("samplemail");
    });

    $("#content").on("click", "#inbox .button.send", function(){
    	history.pushState({type: "inbox", state: "sendmail"}, null, "/userpanel/inbox/sendmail");
    	loadInbox("sendmail");
    });
  
	loadContent();
})