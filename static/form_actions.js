
//auto expand textarea
function adjust_textarea(h) {
    h.style.height = "20px";
    h.style.height = (h.scrollHeight)+"px";
}


$('form').submit(function (event) {
    event.preventDefault()
    $.ajax({
        url: "http://localhost:5000/signup",
	data: $(this).serialize(),
        type: "POST",
        dataType: "html",
        success: function (data) {
	    $('#showresults').val(data);
	    var result = document.getElementById('showresults');
	    result.style.color = "#006400";
        },
        error: function (xhr, status) {
            alert("Sorry, there was a problem!");
        },
        complete: function (xhr, status) {
            //$('#showresults').slideDown('slow')
        }
    });
});
