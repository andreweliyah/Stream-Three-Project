$(function() {
  // basic auth form sign-in/out/up
  $('#auth-form').submit(function(e){
    e.preventDefault()

    $.ajax({
      url: "/api-account-auth/",
      type: "POST",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
      contentType: "application/x-www-form-urlencoded",
      data: $(this).serialize()
    })
    .done(function(data, textStatus, jqXHR) {
      // >>set jwt cookie
      var email = $('#id_email').val();
      if(!email){
        window.location.reload(true);
      }
      var password = $('#auth-form input[id^="id_password"]').eq(0).val();
      $.ajax({
        url: "/api-token-auth/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          "username": email,
          "password": password,
        }),
      })
      .done(function(data, textStatus, jqXHR) {
        window.location.reload(true);
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
        console.log("HTTP Request Failed");
        document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      });
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      data = jqXHR.responseJSON
      $('#messages').text(data['detail'].toUpperCase())
    })
  });

  // >account deletion
  $('#del_account_btn').click(function(e){
    e.preventDefault()
    $('#del_account_confirm').fadeToggle()
  });

  $('#del_account_confirm #del_no').click(function(e){
    e.preventDefault()
    $('#del_account_confirm').fadeOut();
  });

  $('#del_account_confirm #del_yes').click(function(e){
    e.preventDefault()
    $.ajax({
      url: "/api-account-auth/",
      type: "DELETE",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
      },
      contentType: "application/x-www-form-urlencoded",
      data: $(this).serialize()
    })
    .done(function(data, textStatus, jqXHR) {
        window.location.reload(false);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      console.log(jqXHR)
      data = jqXHR.responseJSON
      $('#messages').text(data['Detail'].toUpperCase())
    })
  })

  if(RegExp(/^\/accounts\/signup\//).test(window.location.pathname) || RegExp(/^\/accounts\/login\//).test(window.location.pathname)){
      document.cookie = "csrftoken=''; path=/; expires=Fri, 1 May 1970 23:59:59 GMT"
      document.cookie = "jwtoken=''; path=/; max-age=0; expires=Fri, 1 May 1970 23:59:59 GMT"
  }
});