var reduce = {
  add: function(p, v, nf) {
    // console.log(v)
    // Total number of issues
    p.total.issues++
    
    // total number of days
    if(!p.days[v.modified]){
      p.days[v.modified] = 1;
      p.total.days++;
    }
    else{
      p.days[v.modified]++
    }

   // Total number of weeks
   var first = v.modified.getDate() - v.modified.getDay();
   first = new Date(v.modified.getFullYear(),v.modified.getMonth(),first);
    
   var last = first.getDate() + 6
   last = new Date(v.modified.getFullYear(),v.modified.getMonth(),last);
   
   if(!p.weeks[first+''+last]){
      p.weeks[first+''+last] = 1;
      p.total.weeks ++;
    }
    else{
      p.weeks[first+''+last]++;
    }
    

    // Total number of months
    first = new Date(v.modified.getFullYear(),v.modified.getMonth(),1);

    last = new Date(v.modified.getFullYear(),v.modified.getMonth()+1,1);
    
    if(!p.months[first+''+last]){
      p.months[first+''+last] = 1;
      p.total.months ++;
    }
    else{
      p.months[first+''+last]++;
    }
    
    return p;
  },
  remove: function(p, v, nf) {
    p.total['issues']--;
    
    if(!p.days[v.modified]){
      p.total['days']--;
    }
    else{
      p.days[v.modified]--
    }
    
    // Total number of weeks
    var first = v.modified.getDate() - v.modified.getDay();
    first = new Date(v.modified.getFullYear(),v.modified.getMonth(),first);
    
    var last = first.getDate() + 6
    last = new Date(v.modified.getFullYear(),v.modified.getMonth(),last);

    if(!p.weeks[first+''+last]){
      p.total.weeks --;
    }
    else{
      p.weeks[first+''+last]--;
    }
    

    // Total number of months
    first = new Date(v.modified.getFullYear(),v.modified.getMonth(),1);

    last = new Date(v.modified.getFullYear(),v.modified.getMonth()+1,1);
    
    
    if(!p.months[first+''+last]){
      p.total.months --;
    }
    else{
      p.months[first+''+last]--;
    }
    return p;
  },
  init: function() {
    return {
      total:{
        issues:0,
        days:0,
        weeks:0,
        months:0
      },
      days:{},
      weeks:{},
      months:{}
    };
  }
}

$(function() {
  $('#pager').pagination({
    items: $('#pagercount').val(),
    itemsOnPage: 10,
    cssStyle: 'light-theme',
    onPageClick: pagerdata,
    onInit: pagerdata
  });

  function pagerdata(pageNumber, event){
    if(!pageNumber){
      pageNumber = 1;
    }  
    $.get('/api-tracker/ticket/?page='+pageNumber)
    .done(tableSetup)
  }

  function tableSetup(data){
    var truncate = 20
    // console.log(data)
    $('.manual-add').remove();
    data.forEach(function(d){
      var row =  `<tr class="dc-table-row manual-add">
        <td class="dc-table-column _0">`+d.id+`</td>
        <td class="dc-table-column _1">`+d.type+`</td>
        <td class="dc-table-column _2">`+d.status+`</td>`;
        if(d.description.length>truncate){
          row += `<td class="dc-table-column _3">`+d.description.substring(0,truncate)+` ...</td>`;
        }
        else{
          row += `<td class="dc-table-column _3">`+d.description+`</td>`;
        }
        
        row += `<td class="dc-table-column _4">`+d.votes+`</td>
        <td class="dc-table-column _4"><a href="/tracker/ticket-`+d.id+`/">Go to Ticket</a></td>
      </tr>`;
      $('#all_data').append(row);
    })
  }
});