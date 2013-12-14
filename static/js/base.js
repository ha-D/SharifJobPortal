function relaxUI(){
    $('.ui.checkbox').checkbox();
    $('.ui.radio.checkbox').checkbox();
}

$(document).ready(function(){
	relaxUI();
	$(".footer").load('/footer');
});
