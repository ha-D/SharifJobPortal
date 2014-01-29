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

$(document).ready(function(){
	relaxUI();
	$(".footer").load('/footer');
	$('#confirmbox').modal()

});

function link(href){
    window.location.href = href;
}