
//auto expand textarea
function adjust_textarea(h) {
    h.style.height = "20px";
    h.style.height = (h.scrollHeight)+"px";
}


function render_profile() {
    window.location.href="http://localhost:5000/profile";
}


function render_home() {
    window.location.href="http://localhost:5000/";
    return;
}


function render_edit() {
    window.location.href="http://localhost:5000/edit_profile";
    return;
}


function validate_active() {
    var active_value = $('#active').val()
    if (active_value != "Y" && active_value != "N") {
 	$('#showresults').val("Enter valid values for Active (Y/N)");
	var result = document.getElementById('showresults');
	result.style.color = "#FF0000";
    } else {
 	$('#showresults').val("");
    }
}


function load_edit_pane() {
    $.ajax({
	url: "http://localhost:5000/read_profile",
	data: $('form').serialize(),
	type: "POST",
	dataType: "html",
	success: function (data) {
	    obj = JSON.parse(data)
	    $('#userid').val(obj.user_id);
	    $('#username').val(obj.user_name);
	    $('#password').val(obj.password);
	    $('#passwordexpiry').val(obj.password_expiry);
	    $('#crn').val(obj.crn);
	    $('#profilepassword').val(obj.profile_password);
	    $('#url').val(obj.url);
	    $('#remarks').val(obj.remarks);
	    $('#active').val(obj.is_active);
	    $('#customercarenumber').val(obj.customer_care_number);
	    // var result = document.getElementById('userid');
	    // result.style.color = "#006400";
	},
	error: function (xhr, status) {
	    $('#showresults').val(xhr.responseText);
	    var result = document.getElementById('showresults');
	    result.style.color = "#FF0000";
	},
	complete: function (xhr, status) {
	    //$('#showresults').slideDown('slow')
	}
    });
    $('#edit_pane').show();
}


$('form').submit(function (event) {
    event.preventDefault()
    var formID = event.target.id
    var endpoint = "http://localhost:5000/signup"
    var method = "POST"
    if(formID == "details_form") {
	endpoint = "http://localhost:5000/add_profile"
    } else if(formID == "edit_details_form") {
	endpoint = "http://localhost:5000/get_apps_list"
    }
    $.ajax({
	url: endpoint,
	data: $(this).serialize(),
	type: method,
	dataType: "html",
	success: function (data) {
	    if(formID == "edit_details_form") {
		html = "";
		obj = JSON.parse(data)
		for(const app of obj.apps_list) {
		    html += "<option value=" + app  + ">" +app + "</option>"
		}
		document.getElementById("app_name").innerHTML = html;
		load_edit_pane();
	    } else {
		$('#showresults').val(data);
		var result = document.getElementById('showresults');
		result.style.color = "#006400";
	    }
	},
	error: function (xhr, status) {
	    $('#showresults').val(xhr.responseText);
	    var result = document.getElementById('showresults');
	    result.style.color = "#FF0000";
	},
	complete: function (xhr, status) {
	    //$('#showresults').slideDown('slow')
	}
    });
});


$(".toggle-password").click(function() {

  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});
