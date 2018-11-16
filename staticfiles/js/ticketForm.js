$('form#ticketform').submit(function(e){
  e.preventDefault();
  tinyMCE.triggerSave();
  var data = {"type": $('#id_type').val(), "description": $('#id_description').val()}
  $.ajax({
    url: '/api-tracker/ticket/',
    type: 'post',
    dataType: 'json',
    data: data
  })
  .done(function(data,data2,data3) {   
    window.location.assign('/tracker/ticket-'+data.id+'/');
  })
  .fail(function(jqXHR, textStatus, errorThrown) {
    data = jqXHR.responseJSON
    // console.error(errorThrown)
    if(errorThrown == "Payment Required"){
      $('#messages').text('You must be subcribed to submit a feature request'.toUpperCase()).html('You must be subcribed to submit a feature request.'.toUpperCase() + ' <a href="/accounts/settings/">'+'Click here to subcribe.'.toUpperCase()+'</a>')
    }
  });       
});