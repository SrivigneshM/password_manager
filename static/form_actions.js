
const app_base_url = "https://simvault.com:5000/";

//auto expand textarea
function adjust_textarea(h) {
    h.style.height = "20px";
    h.style.height = (h.scrollHeight)+"px";
}


function html_url(endpoint) {
    window.location.href=app_base_url + endpoint;
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


function ajax_call(formID, endpoint, method, action) {
    $.ajax({
	url: endpoint,
	data: $('#'+formID).serialize(),
	type: method,
	dataType: "html",
	success: function (data) {
	    if(action == "load_drop_down") {
		html = "";
		obj = JSON.parse(data)
		for(const app of obj.apps_list) {
		    html += "<option value='" + app  + "'>" +app + "</option>"
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
		$('#is_active').prop('checked', false);
                if (obj.is_active == 'on') {
		    $('#is_active').prop('checked', true);
		}
		$('#customercarenumber').val(obj.customer_care_number);
            } else if (action == "login") {
                html_url('profile');
	    } else if (action == "add" || action == "update") {
		var message = document.getElementById('showresults');
                message.classList.remove('is-hidden');
	        message.classList.remove('is-danger');
	        message.classList.add('is-success');
		var output = "<p>" + data + "</p>"
		message.innerHTML = output;
                scroll_up();
	    } else {
		html_url('login');
	    }
	},
	error: function (xhr, status) {
	    var result = document.getElementById('showresults');
	    result.classList.remove('is-hidden');
	    result.classList.remove('is-success');
	    result.classList.add('is-danger');
	    var output = "<p>" + xhr.responseText + "</p>"
	    result.innerHTML = output;
            scroll_up();
	},
	complete: function (xhr, status) {
	    //$('#showresults').slideDown('slow')
	}
    });
}


function scroll_up() {
    window.scroll({
      top: 0,
      left: 0,
      behavior: 'smooth'
    });
}


function load_edit_pane() {
    ajax_call("edit_form", app_base_url + "read_profile", "POST", "load_edit_pane");
    $('#edit_pane').show();
}


$('form').submit(function (event) {
    event.preventDefault()
    var formID = event.target.id
    var endpoint = app_base_url + "signup";
    var method = "POST"
    var action = ""
    if (formID == "login_form") {
	endpoint = app_base_url + "login";
	action = "login"
    } else if(formID == "details_form") {
	endpoint = app_base_url + "add_profile";
	action = "add"
    } else if(formID == "edit_form") {
	endpoint = app_base_url + "add_profile";
	action = "update"
	method = "PUT"
    }
    ajax_call(formID, endpoint, method, action)
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


const tabs = document.querySelectorAll('.tabs li');
const tabContentBoxes = document.querySelectorAll('#tab-content > div');

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach(item => item.classList.remove('is-active'))
    tab.classList.add('is-active');

    const target = tab.dataset.target;
    tabContentBoxes.forEach(box => {
	if (box.getAttribute('id') === target) {
	  box.classList.remove('is-hidden');
	} else {
	  box.classList.add('is-hidden');
	}
    });
    if (target == "edit") {
	endpoint = app_base_url + "get_apps_list";
	action = "load_drop_down"
	ajax_call("details_form", endpoint, "GET", action);
    }
  })
})
