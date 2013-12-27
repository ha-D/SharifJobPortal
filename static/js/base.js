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

$(document).ready(function(){
	relaxUI();
	$(".footer").load('/footer');
});

