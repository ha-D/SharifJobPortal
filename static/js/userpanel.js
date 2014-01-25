// var userpanel = {}

// userpanel.init = function(){
// 	userpanel.currentPage = 'main';

// 	Sammy(function() {
// 		this.get("#inbox/message/:id", function(){
// 			var id = this.params.id;
// 			function done(){
// 				userpanel.loadInbox("message/" + id);
// 			}

// 			if(userpanel.currentPage != 'inbox')
// 				userpanel.loadContent('inbox', done);
// 			else
// 				done();
// 		});

// 		this.get("#inbox/:page", function(){
// 			var page = this.params.page;
// 			function done(){
// 				userpanel.loadInbox(page);
// 			}

// 			if(userpanel.currentPage != 'inbox')
// 				userpanel.loadContent('inbox', done);
// 			else
// 				done();
// 		});

// 		this.get('#:page', function() {
// 			var page = this.params.page;
// 			if(page == 'inbox'){
// 				location.hash = 'inbox/list';
// 				return;
// 			}

// 			userpanel.loadContent(page);
// 		});

// 		this.get('', function() { 
// 			userpanel.loadContent();
// 		});
// 	}).run();
// }

// userpanel.loadContent = function(content, done){
// 	if(content == null || content.trim().length == 0)
// 		content = 'main';

// 	console.log("Loading  " + content);

// 	$("#dimmer").dimmer("show");
// 	setTimeout(function(){
// 		$.ajax({
// 			url: "/userpanel/ajax/" + content +"/",
// 			dataType: 'json',
// 			success: function(result){
// 				if(result.result == 1){
// 					$("#content").html(result.data);
// 					userpanel.currentPage = content;
// 					if(done)
// 						done();	
// 				}else if(result.error = "unauthorized"){
// 					location = result.data;
// 				}
// 			},
// 			error: function(){

// 			},
// 			complete: function(){
// 				$("#dimmer").dimmer("hide");
// 			}
// 		})		
// 	}, 200);
// }

// userpanel.loadInbox = function(content){
// 	if(content == null || content.trim().length == 0)
// 		content = 'list';

// 	console.log("Loading Inbox  " + content);

// 	$("#inbox-dimmer").dimmer("show");
// 	setTimeout(function(){
// 		$.ajax({
// 			url: "/userpanel/ajax/inbox/" + content +"/",
// 			dataType: 'json',
// 			success: function(result){
// 				if(result.result == 1){
// 					$("#inbox-content").html(result.data);
// 				}else if(result.error == 'unauthorized'){
// 					locatoin = result.data;
// 				}
// 			},
// 			error: function(){

// 			},
// 			complete: function(){
// 				$("#inbox-dimmer").dimmer("hide");
// 			}
// 		})		
// 	}, 200);
// }

$(function(){
	// $("#dimmer").dimmer({
	// 	duration: {
	// 		show: 700,
	// 		hide: 1000
	// 	}
	// });

	$("#content").on("click", "#inbox tr", function(){
		var mid = $(this).attr('data-message-id');
		// location.hash = "inbox/message/" + mid;
		location = "/userpanel/inbox/" + mid +"/"
	});

	$("#content").on("click", "#inbox .button.send", function(){
		location = "/userpanel/inbox/send/"
	});

    $("#sendMail").click(function(){sendEmail()});

    $("#userpanel #friends_search .search").click(function(){searchFriends();});
})

function sendEmail(){
    console.log('sending email...');

    var ajaxData = {
        "recipient" : $("#recipient").val(),
        "subject" : $("#subject").val(),
        "message" : $("#message").val()
    };


    $.ajax({
        url : "sendEmail",
        type : 'post',
        dataType : 'json',
        data : ajaxData,
        success : function(data, status, xhr) {
            if (data.result == 0) {
                // Request error
                console.log("error");
            } else {
                console.log("hello??");
                console.log('status = ' + data.status)
                if ( data.status == 'fail')
                    alert(data.error);
            }
        },
        error: function(){
            console.log('gand khord');
        },
        complete: function(){
            location = "/userpanel/inbox/list/";
        }
    });

}

function sendFriendShipRequest(invited_user){
    console.log('invited user is ' + invited_user)

    var ajaxData = {
        "invitedUser" : invited_user

    };
    $.ajax({
        url : "requestFriendShip",
        type : 'post',
        dataType : 'json',
        data : ajaxData,
        success : function(data, status, xhr) {
            if (data.result == 0) {
                // Request error
                console.log("error");
            } else {
                alert(data.status)
            }
        },
        error: function(){
            console.log('gand khord');
            alert('ajax gand khord');
        }
    });
}

function searchFriends(){
    $("#friends_search").children().slice(1).remove();

    var ajaxData = {
        "name" : $("#friends_search input").val()
    };
    $.ajax({
        url : "search",
        type : 'post',
        dataType : 'json',
        data : ajaxData,
        success : function(data, status, xhr) {
            if (data.result == 0) {
                // Request error
                console.log("error");
            } else {
                console.log("liste adama daryaft shod");
                friends = data.friends;
                console.log(friends);
                for(var i in friends){
                    $("<div class = 'ui segment borderless'></div>").appendTo($("#friends_search"));
                    $("<img class='rounded ui image' src=" + friends[i].pic + ">").appendTo($("#friends_search .segment").last());
                    $("<div class='nametag'>" + friends[i].name + "</div>").appendTo($("#friends_search .segment").last());
                    if ( friends[i].isFriend == false){
                        $("<div _id=" + friends[i].id + " class='mini red circular ui button'>دعوت به دوستی</div>").appendTo($("#friends_search .segment").last()).click(
                            function(event){
                                sendFriendShipRequest(event.target.getAttribute('_id'));
                            });
                    }
                }
                if (friends.length ==0){
                    $("<div class='ui segment borderless'> هیچ نتیجه ای پیدا نشد!</div>").appendTo($("#friends_search"));
                }
            }
        },
        error: function(){
            console.log('gand khord');
            alert('ajax gand khord');
        }
    });


}