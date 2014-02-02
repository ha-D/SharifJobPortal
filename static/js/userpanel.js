$(function(){
	$("#content").on("click", "#inbox tr", function(){
		var mid = $(this).attr('data-message-id');
		location = "/userpanel/inbox/" + mid +"/"
	});

	$("#content").on("click", "#inbox .button.send", function(){
		location = "/userpanel/inbox/send/"
	});

    $("#sendMail").click(function(){sendEmail()});

    $(window).bind('scroll', function() {
        if ($("#userpanel").height() - 500 < 0|| $(window).scrollTop() < $("#userpanel").height() - 500) {
                $('#panelmenu').addClass('fixed');
                $('#panelmenu').css('top', '');
        } else {
            if($('#panelmenu').hasClass('fixed')){
                $('#panelmenu').css('top', $(window).scrollTop());
            }
            $('#panelmenu').removeClass('fixed');
        }
    });   
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

        }
    }); 
}
