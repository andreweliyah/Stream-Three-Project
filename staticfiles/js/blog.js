$(function() {
  $('form#postform').submit(function(e){
    e.preventDefault();
    if(RegExp('edit$').test(document.location.pathname)){
      var type = 'PUT';
    }
    else{
      var type = 'POST';
    }
    var data = new FormData($('form#postform')[0]);
    $.ajax({
      url: '/api-blog/?format=json',
      type: type,
      cache: false,
      enctype: 'multipart/form-data',
      contentType: false,
      processData: false,
      dataType: 'json',
      data: data
    })
    .done(function(data,status,data3) {
      window.location.assign('/blog/post-'+data.id+'/')
    });
  });

  // >Delete post
  $('#del_post_confirm').submit(function(e){
    e.preventDefault();
  });

  $('#del_post_btn').click(function(e){
    // Show post delete confirmation
    e.preventDefault();
    $('#del_post_confirm').slideToggle();
  });

  $('#del_post_confirm #del_no').click(function(e){
    // Cancel post deletion and hide confirm section
    e.preventDefault();
    $('#del_post_confirm').slideUp();
  });

  $('#del_post_confirm #del_yes').click(function(e){
    e.preventDefault();
    var trying = 0;
    var retries = 3
    var retry = setInterval(function(){
      var id = document.location.pathname.split('-')[1].split('/')[0];
      $.ajax({
        url: '/api-blog/',
        type: 'delete',
        contentType: "application/json",
        data: JSON.stringify({id: id})
      })
      .always(function(data,status,data3) {
        trying++; 
        if(status == 'success' || trying >= retries){
          window.location.assign('/blog/')
          clearInterval(retry); 
        }
      });
    },1000);
  });
});