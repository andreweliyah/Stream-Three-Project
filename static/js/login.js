$(function() {
  $('#login-form').submit(function(e){
    e.preventDefault();
    var url = e.target.action;
    var data = {username: $('input#id_email').val(),
                password: $('input#id_password').val()}; // user crediintials
    $.post(url,$(this).serialize())
    .done(function(){
      $.post('/api-token-auth/',data)
      .done(function(d){
        $.get('/api-token-auth/',function(){
          // $('#login-form').submit();
          location.reload(true);
        });
        
      })
      .fail(function(d,e){
        $('#messages').text('Username or password incorrect.');
      });
    })
    .fail(function(){
      console.log('wrong')
    })
  });
});