    var form_data = $(this).serialize();
// $(function() {
  // basic auth form sign-in/out/up
  $('#auth-form').submit(function(e){
    e.preventDefault()

    var post_url;
    var form_data = $(this).serialize();
    console.log(form_data)
    if($('#id_password')){
      console.log('pass')
      post_url='/accounts/login/'
      var email = $('#id_email').val();
      if(!email){
        window.location.reload(true);
      }
      var password = $('#id_password').val();
      $.ajax({
        url: "/api-token-auth/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          "username": email,
          "password": password,
        })
      })
      .done(function(data, textStatus, jqXHR) {
        $.ajax({
          url: post_url,
          type: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
          },
          contentType: "application/x-www-form-urlencoded",
          data: form_data
        })
        .done(function(data, textStatus, jqXHR) {
          window.location.reload(true);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
          if(jqXHR.status==400)
          {
            $('#messages').text('Username and/or Password are incorrect.')
          }
          if(jqXHR.status==403)
          {
            $('#messages').text('Authentication Error. Try reloading the page and try again.')
          }
          
          console.log(jqXHR.status)
          console.log(textStatus)
          console.log(errorThrown)
          console.log("HTTP Request Failed");
          // document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
          // document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        });
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
        if(jqXHR.status==400)
        {
          $('#messages').text('Username and/or Password are incorrect.')
        }
        
        console.log(jqXHR.status)
        console.log(textStatus)
        console.log(errorThrown)
        console.log("HTTP Request Failed");
        // document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        // document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      });
    }



    // $.ajax({
    //   url: post_url,
    //   type: "POST",
    //   headers: {
    //       "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    //   },
    //   contentType: "application/x-www-form-urlencoded",
    //   data: $(this).serialize()
    // })
    // .done(function(data, textStatus, jqXHR) {
    //   // >>set jwt cookie
    //   var email = $('#id_email').val();
    //   if(!email){
    //     window.location.reload(true);
    //   }
    //   var password = $('#auth-form input[id^="id_password"]').eq(0).val();
    //   $.ajax({
    //     url: "/api-token-auth/",
    //     type: "POST",
    //     contentType: "application/json",
    //     data: JSON.stringify({
    //       "username": email,
    //       "password": password,
    //     }),
    //   })
    //   .done(function(data, textStatus, jqXHR) {
    //     window.location.reload(true);
    //   })
    //   .fail(function(jqXHR, textStatus, errorThrown) {
    //     if(jqXHR.status==400)
    //     {
    //       $('#messages').text('Username and/or Password are incorrect.')
    //     }
        
    //     console.log(jqXHR.status)
    //     console.log(textStatus)
    //     console.log(errorThrown)
    //     console.log("HTTP Request Failed");
    //     // document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    //     // document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    //   });
    // })
    // .fail(function(jqXHR, textStatus, errorThrown) {
    //   console.log(errorThrown)
    //   data = jqXHR.responseJSON
    //   $('#messages').text(data['detail'].toUpperCase())
    // })
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
});