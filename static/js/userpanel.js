
function loadContent(content){
	if(content === undefined || content.trim().length == 0)
		content = 'main';

	console.log("Loading  " + content);

	$("#dimmer").dimmer("show");
	setTimeout(function(){
		$.ajax({
			url: "/ajax/userpanel/" + content,
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

$(document).ready(function(){
	// $("#dimmer").dimmer({
	// 	duration: {
	// 		show: 700,
	// 		hide: 1000
	// 	}
	// });

	// $("#panelmenu .item").click(function(){
	// 	loadContent($(this).attr("page"));
	// });

	var app = Davis(function () {
		this.configure(function () {
		    this.generateRequestOnPageLoad = true
		})
		this.get('/userpanel/', function (req) {
			loadContent();
		})
		this.get('/userpanel/:name', function (req) {
			loadContent(req.params['name']);
		})
	})

    app.start()


    $("#content").on("click", "#inbox tr", function(){
    	window.location = "/userpanel/samplemail";
    });
})