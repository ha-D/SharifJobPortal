$(function(){
	$("#content").on("click", "#inbox tr", function(){
		var mid = $(this).attr('data-message-id');
		location = "/userpanel/inbox/" + mid +"/"
	});

	$("#content").on("click", "#inbox .button.send", function(){
		location = "/userpanel/inbox/send/"
	});

    $("#sendMail").click(function(){sendEmail()});

    $("#userpanel #friends_search .search").click(function(){searchFriends();});

    $(".acceptFriendShip").click(function(e){
       var friendId = $(this).attr("_id");
        response_to_FriendShip(e.target , friendId , true);
    });

    $(".rejectFriendShip").click(function(e){
        var friendId = $(this).attr("_id");
        response_to_FriendShip(e.target , friendId , false);
    });


})

function response_to_FriendShip(ee , friendId , fstatus){
    console.log('inja seda zade shod???');
    var ajaxData = {
        "friendID" : friendId,
        "accepted" : fstatus
    };
    $.ajax({
        url : "responseToFriendShip",
        type : 'post',
        dataType : 'json',
        data : ajaxData,
        success : function(data, status, xhr) {
            if (data.result == 0) {
                // Request error
                console.log("error");
            } else {
                console.log('success');
                ee.parentElement.remove();


                if (fstatus==true){
                    $("<div class = 'ui segment borderless'></div>").appendTo($("#friends_list"));
                    $("<img class= 'rounded ui image' src=" + data.image + ">").appendTo($("#friends_list .segment").last());
                    $("<div class='ui pointing label'>" + data.name + "</div>").appendTo($("#friends_list .segment").last());

                }


            }
        },
        error: function(){
            console.log('error in response to friendShip function');
        }
    });



}

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
        type : 'get',
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
