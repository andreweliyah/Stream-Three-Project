$(function(){

  // $('#del_account_confirm').submit(function(e){
  //   e.preventDefault();
  // })
  // Delete Account
  $('#del_account_btn').click(function(e) {
    // Show account delete confirmation
    e.preventDefault();
    $('#del_account_confirm').show();
  });

  $('#del_no').click(function(e) {
    // Cancel account deletion and hide confirm section
    e.preventDefault();
    $('#del_account_confirm').hide();
  });

  $('#del_yes').click(function(e) {
    // Confirm account deletion and delete account
    // e.preventDefault();
    // $.ajax({
    //   url: "/api-account-auth/",
    //   type: "DELETE",
    //   headers: {
    //       "Content-Type": "application/json; charset=utf-8",
    //       "Authorization": "JWT "+$('#token').val()
    //   },
    //   contentType: "application/json",
    // })
    // .done(function() {
    //   location.reload(true);
    // })
    // .fail(function() {
    //   console.error("Error recieving token");
    // })
  });
});