$.validator.setDefaults({
  submitHandler: function() { 
    var params = "author=" + $("#author").val();
    params = params + "&title=" + $("#title").val();
    var inst = $("input[@name='school']:checked").val();
    if ( inst == "UFRJ" ) {
      params = params + "&school=Universidade Federal do Rio de Janeiro";
      params = params + "&dept=" + $("#dept").val();
    } else {
      params = params + "&school=" + $("#schoolname").val();
      params = params + "&dept=" + $("#otherdept").val();;
    }
    params = params + "&degree=" + $("#degree").val();

    $.ajax({
      type: "GET",
      url: "users.php",
      data: params,
      success: function(xml) {
        setTimeout(function(){
        $("#loading").hide();
        $("#response_to_submission").show("fast");
        },
        1500);
      }
    });
  }
});

$(document).ready(function() {
  $("#user_data")[0].reset();
  $("#response_to_submission").hide();
  $('#loading').hide();

  $('#otherdept').hide();
  $('#otherdept').attr('disabled', 'disabled');
  $('#schoolname').attr('disabled', 'disabled');
  $('#ufrj').attr('checked', 'checked');
  $('#dept').removeAttr('disabled');
  $('#dept').show();

  $('#loading').ajaxStart(function() {
      $(this).show();
  });
  $("#user_data").ajaxStop(function() {
      $(this).hide("fast");
  });
  $("#user_data").validate();

  $("input[name='school']").click(function(){
    if ($(this).val() == "UFRJ") {
      $('#otherdept').hide();
      $('#otherdept').attr('disabled', 'disabled');
      $('#schoolname').attr('disabled', 'disabled');
      $('#dept').removeAttr('disabled');
      $('#dept').show();
    } else {
      $('#dept').hide();
      $('#dept').attr('disabled', 'disabled');
      $('#otherdept').removeAttr('disabled');
      $('#otherdept').show();
      $('#schoolname').removeAttr('disabled');
    }
  });
});

function restoreDefaults() {
  $('#otherdept').hide();
  $('#otherdept').attr('disabled', 'disabled');
  $('#schoolname').attr('disabled', 'disabled');
  $('#dept').removeAttr('disabled');
  $('#dept').show();
}
