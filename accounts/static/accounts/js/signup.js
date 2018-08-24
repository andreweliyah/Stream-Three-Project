$(function() {
  $('#signup-form').submit(function(e){
    e.preventDefault();
    var url = e.target.action;
    var data = {username: $('input#id_email').val(),
                password: $('input#id_password1').val()}; // user crediintials
    $.post(url,$(this).serialize())
    .done(function(){
      $.post('/api-token-auth/',data)
      .done(function(d){
        console.log(d)
        $(this).submit()
        location.reload(true);
      })
      .fail(function(d){
        $('#messages').text('User already exists')
      });
    })
    .fail(function(d){
      console.log(d)
    });
  });
});