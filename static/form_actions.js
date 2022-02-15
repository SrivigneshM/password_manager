    
//auto expand textarea
function adjust_textarea(h) {
    h.style.height = "20px";
    h.style.height = (h.scrollHeight)+"px";
}

// function submit_form(){
//     $(document).on('submit', '#password_form', function() {
// 	$.post("http://localhost:5000/password", $(this).serialize(), function(response){
// 	    window.alert(response)
// 	},'json');
// 	return false;
//     });
// }

$(document).ready(function(){
    var $form = $('form');
    $form.submit(function(){
	$.post("http://localhost:5000/password", $(this).serialize(), function(response){
	    console.log(response)
	},'json');
	return false;
    });
});

