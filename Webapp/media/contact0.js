jQuery(function() {
  jQuery('.error').hide();
  jQuery(".button").click(function() {
		// validate and process form
		// first hide any error messages
    jQuery('.error').hide();
		
	  var name = jQuery("input#name").val();
		if (name == "") {
      jQuery("span#name_error").show();
      jQuery("input#name").focus();
      return false;
    }
	  var email = jQuery("input#email").val();
	  if (email == "") {
      jQuery("span#email_error").show();
      jQuery("input#email").focus();
      return false;
    }
	
	var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	if(!emailReg.test(email)) {
	jQuery("span#email_error2").show();
    jQuery("input#email").focus();
      return false;
	}
	
	  var web = jQuery("input#web").val();
		if (web == "") {
      jQuery("input#web").focus();
      return false;
    }
	
	  var msg = jQuery("textarea#msg").val();
	  if (msg == "") {
	  jQuery("span#msg_error").show();
	  jQuery("textarea#msg").focus();
	  return false;
    }
		
		var dataString = 'name='+ name + '&email=' + email + '&web=' + web + '&msg=' + msg;
		//alert (dataString);return false;
		
	  jQuery.ajax({
      type: "POST",
      url: "process.php",
      data: dataString,
      success: function() {
        jQuery('#contactform').html("<div id='message'></div>");
        jQuery('#message').html("<strong>Contact Form Submitted!</strong>")
        .append("<p>We will be in touch soon.</p>")
        .hide()
        .fadeIn(1500, function() {
          jQuery('#message');
        });
      }
     });
    return false;
	});
});

jQuery(function() {
  jQuery('.error').hide();
  jQuery(".button_foot").click(function() {
		// validate and process form
		// first hide any error messages
    jQuery('.error').hide();
		
	  var f_name = jQuery("input#f_name").val();
		if (f_name == "") {
      jQuery("span#f_name_error").show();
      jQuery("input#f_name").focus();
      return false;
    }
	  var f_email = jQuery("input#f_email").val();
	  if (f_email == "") {
      jQuery("span#f_email_error").show();
      jQuery("input#f_email").focus();
      return false;
    }
	
	var f_emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	if(!f_emailReg.test(f_email)) {
	jQuery("span#f_email_error2").show();
    jQuery("input#f_email").focus();
      return false;
	}
	  var f_msg = jQuery("textarea#f_msg").val();
	  if (f_msg == "") {
	  jQuery("span#f_msg_error").show();
	  jQuery("textarea#f_msg").focus();
	  return false;
    }
		
		var dataString = 'f_name='+ f_name + '&f_email=' + f_email + '&f_msg=' + f_msg;
		//alert (dataString);return false;
		
	  jQuery.ajax({
      type: "POST",
      url: "process.php",
      data: dataString,
      success: function() {
        jQuery('#footercontactform').html("<div id='message'></div>");
        jQuery('#message').html("<strong>Contact Form Submitted!</strong>")
        .append("<p>We will be in touch soon.</p>")
        .hide()
        .fadeIn(1500, function() {
          jQuery('#message');
        });
      }
     });
    return false;
	});
});

