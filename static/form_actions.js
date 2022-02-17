
//auto expand textarea
function adjust_textarea(h) {
    h.style.height = "20px";
    h.style.height = (h.scrollHeight)+"px";
}


$('form').submit(function (event) {
    event.preventDefault()
    $.ajax({
        url: "http://localhost:5000/password",
	data: $(this).serialize(),
        type: "POST",
        dataType: "html",
        success: function (data) {
	    $('#showresults').val(data);
        },
        error: function (xhr, status) {
            alert("Sorry, there was a problem!");
        },
        complete: function (xhr, status) {
            //$('#showresults').slideDown('slow')
        }
    });
});
