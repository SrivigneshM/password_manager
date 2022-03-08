
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


function ajax_call(endpoint, method, action) {
    $.ajax({
	url: endpoint,
	data: $('form').serialize(),
	type: method,
	dataType: "html",
	success: function (data) {
	    if(action == "load_drop_down") {
		html = "";
		obj = JSON.parse(data)
		for(const app of obj.apps_list) {
		    html += "<option value=" + app  + ">" +app + "</option>"
		}
		document.getElementById("app_name").innerHTML = html;
		load_edit_pane();
	    } else if (action == "load_edit_pane") {
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
}


function load_edit_pane() {
    ajax_call("http://localhost:5000/read_profile", "POST", "load_edit_pane");
    $('#edit_pane').show();
}


function update_profile() {
    ajax_call("http://localhost:5000/add_profile", "PUT", "");
}


$('form').submit(function (event) {
    event.preventDefault()
    var formID = event.target.id
    var endpoint = "http://localhost:5000/signup"
    var method = "POST"
    var action = ""
    if(formID == "details_form") {
	endpoint = "http://localhost:5000/add_profile"
    } else if(formID == "edit_details_form") {
	endpoint = "http://localhost:5000/get_apps_list"
	action = "load_drop_down"
    }
    ajax_call(endpoint, "POST", action)
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
