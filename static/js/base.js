function relaxUI(){
    $('.ui.checkbox').checkbox();
    $('.ui.radio.checkbox').checkbox();

    $('.ui.dropdown').dropdown();
}

$(document).ready(function(){
	relaxUI();
	$(".footer").load('/footer');
});

