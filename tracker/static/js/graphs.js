'use strict';

d3.json('/api-tracker/ticket/').then(function(serverdata){
  // >fix color scheme issues
  dc.config.defaultColors(d3.schemeSet1)

  // >format data
  function formatData(data,truncate) {
    var dateFormatSpecifier = '%Y-%m-%d';
    var dateFormat = d3.timeFormat(dateFormatSpecifier);
    var dateFormatParser = d3.timeParse(dateFormatSpecifier)

    data.forEach(function(d,i){
      
      if(data[i].description.length>truncate)
      {
        data[i].description = data[i].description.substring(0,truncate)+' ...';
      }
      data[i].modified = dateFormatParser(data[i].modified);
      data[i].link = '<a href="/tracker/ticket-'+data[i].id+'/">Go to Ticket</a>';
    });
    return data
  }

  // >reduce function
  var reduce = {
    add: function(p, v, nf) {
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

  // >variables
  // >>settings
  var offset = 0; // for pager
  var pageLimit = 10; // for pager
  var truncate = 20;
  var active = []; // container for all active tickets
  var activeBugs = []; // container for top 5 active bug tickets
  var activeFeatures = []; // container for top 5 active feature tickets
  var completeTickets = []; // container for all complete tickets

  // >>elements
  var number = dc.numberDisplay('#number');
  var statusSelectField = dc.selectMenu('#status-select');
  var typeSelectField = dc.selectMenu('#type-select');
  var fullDataTable = dc.dataTable('#fulllist');
  var smallDataTable = dc.dataTable('#smalllist');
  var idSearchField = dc.textFilterWidget('#id-field');
  var descriptionSearchField = dc.textFilterWidget('#search-field');
  var dayAvg = dc.numberDisplay('#day-avg');
  var weekAvg = dc.numberDisplay('#week-avg');
  var monthAvg = dc.numberDisplay('#month-avg');
  var typeComplete = dc.pieChart('#type-complete');
  var featureVoteChart = dc.dataTable('#vote-feature');
  var featureVoteChartSmall = dc.dataTable('#vote-feature-small');
  var bugVoteChart = dc.dataTable('#vote-bug');
  var bugVoteChartSmall = dc.dataTable('#vote-bug-small');

  // >>formated data
  var masterdata = formatData(serverdata,truncate);

  // >>crossfilters
  var ndx = crossfilter(masterdata);
  var ndx2;
  var ndx3;
  var ndx4;
      
  // >>crossfilter groups
  var all = ndx.groupAll();
  var allcomplete;

  // >>dimensions
  var typeDim = ndx.dimension(dc.pluck('type'));
  var idDim = ndx.dimension(dc.pluck('id'));
  var statusDim = ndx.dimension(dc.pluck('status'));
  var desDim = ndx.dimension(dc.pluck('description'));
  var completeStatusDim;
  var featureTicketDim;
  var bugTicketDim;

  // >>group setup
  var typeGroup = typeDim.group();
  var statusGroup = statusDim.group();
  var desGroup = desDim.group();
  var completeStatusGroup;

  // >setup active and complete tickets data
  masterdata.forEach(function(d){ 
    if(d.status == 'TODO' || d.status == 'DOING'){
      if(d.type == 'BUG'){
        activeBugs.push(d);
      }
      else{
        activeFeatures.push(d);
      }
    }
    else{
      completeTickets.push(d);
    }

    if(d.status == 'DONE' || d.status == 'DOING'){
      active.push(d);
    }
  });

  // >>sort active tickts by votes
  activeFeatures.sort(function(a,b){
    if(a.votes > b.votes){
      return 1
    }
    else if(a.votes < b.votes){
      return -1
    }
    return 0
  });
  activeBugs.sort(function(a,b){
    if(a.votes > b.votes){
      return 1
    }
    else if(a.votes < b.votes){
      return -1
    }
    return 0
  });

  // >>save only top 5 voted tickets
  activeBugs.splice(4,activeBugs.length-5)
  activeFeatures.splice(4,activeFeatures.length-5)

  // >>arrange votes from high to low
  activeFeatures.reverse();
  activeBugs.reverse();

  // >chart setup
  ndx2 = crossfilter(completeTickets);
  ndx3 = crossfilter(activeFeatures);
  ndx4 = crossfilter(activeBugs);      

  allcomplete = ndx2.groupAll().reduce(reduce.add,reduce.remove,reduce.init);

  completeStatusDim = ndx2.dimension(dc.pluck('type'));
  featureTicketDim = ndx3.dimension(dc.pluck('type'));
  bugTicketDim = ndx4.dimension(dc.pluck('type'));

  completeStatusGroup = completeStatusDim.group();

  featureTicketDim.filter('FEATURE');
  bugTicketDim.filter('BUG');

  // >averages
  // >>day
  dayAvg
  .group(allcomplete)
  .formatNumber(d3.format(".1s"))
  .valueAccessor(function(d) {
    return d.total.issues/d.total.days;
   })
  .html({
    one:"<span>%number</span> ticket a day complete",
    some:"<span>%number</span> tickets a day complete"
  })

  // >>week
  weekAvg
  .group(allcomplete)
  .formatNumber(d3.format(".1s"))
  .valueAccessor(function(d) {
    return d.total.issues/d.total.weeks;
   })
  .html({
    one:"<span>%number</span> ticket a week complete",
    some:"<span>%number</span> tickets a week complete"
  })

  // >>month
  monthAvg
  .group(allcomplete)
  .formatNumber(d3.format(".1s"))
  .valueAccessor(function(d) {
    return d.total.issues/d.total.months;
   })
  .html({
    one:"<span>%number</span> ticket a month complete",
    some:"<span>%number</span> tickets a month complete"
  })

  // >complete pie chart
  typeComplete
  .dimension(completeStatusDim)
  // .width('200')
  // .radius(400)
  .minWidth(100)
  .group(completeStatusGroup)
  .label(function (d) {
    return d.key+': '+Math.floor(d.value*100/completeTickets.length)+'%'
  });

  // >filters
  // >>id
  idSearchField
  .dimension(idDim)
  .normalize(function(s){
    return s.toString();
  })
  .placeHolder('Enter ID');
  
  // >>type
  typeSelectField
  .dimension(typeDim)
  .group(typeGroup);

  // >>status
  statusSelectField
  .dimension(statusDim)
  .group(statusGroup);
  
  // >>description search field
  descriptionSearchField
  .dimension(desDim);

  // >data table
  // >>full
  fullDataTable
  .dimension(idDim)
  .group(function(d){
    return 'All';
  })
  .columns([
    "id",
    "type",
    "status",
    "description",
    "votes",
    "link"
  ]);

  //>>small
  smallDataTable
  .dimension(idDim)
  .group(function(d){
    return 'All';
  })
  .columns([
    "type",
    "description",
    "link"
  ]); 

  // >Top Voted
  // >>feature
  // >>>full
  featureVoteChart
  .dimension(featureTicketDim)
  .group(function(d){
    return 'TOP 5 '+d.type+'S';
  })
  .columns([
    'id',
    'status',
    'description',
    'votes',
    'link'
  ])
  .sortBy(function (d) {
    return d.votes;
  })
  .order(d3.descending)
  .size(5);

  // >>>small
  featureVoteChartSmall
  .dimension(featureTicketDim)
  .group(function(d){
    return 'TOP 5 '+d.type+'S';
  })
  .columns([
    'type',
    'description',
    'link'
  ])
  .sortBy(function (d) {
    return d.votes;
  })
  .order(d3.descending)
  .size(5);

  // >>bug
  // >>>full
  bugVoteChart
  .dimension(bugTicketDim)
  .group(function(d){
    return 'TOP 5 '+d.type+'S';
  })
  .columns([
    'id',
    'status',
    'description',
    'votes',
    'link'
  ])
  .sortBy(function (d) {
    return d.votes;
  })
  .order(d3.descending)
  .size(5);

  // >>>small
  bugVoteChartSmall
  .dimension(bugTicketDim)
  .group(function(d){
    return 'TOP 5 '+d.type+'S';
  })
  .columns([
    'type',
    'description',
    'link'
  ])
  .sortBy(function (d) {
    return d.votes;
  })
  .order(d3.descending)
  .size(5);

  number
  .group(all)
  .formatNumber(d3.format(""))
  .valueAccessor(function(d) {
    fullDataTable
    .beginSlice(0)
    .endSlice(pageLimit);
    smallDataTable
    .beginSlice(0)
    .endSlice(pageLimit);
    $(function() {
      $('#pager').pagination('updateItems', d);
      $('#pager').pagination('selectPage', 1);
      // fullDataTable.redraw();
      fullDataTable
      .beginSlice(0)
      .endSlice(pageLimit);
      smallDataTable
      .beginSlice(0)
      .endSlice(pageLimit);
    });
    return d
   })
  .html({
    one:"<span>%number</span> ticket",
    some:"<span>%number</span> tickets",
    none:"<span>0</span> tickets"
  })
                            
  dc.renderAll();
  $( window ).resize(function() {
    dc.renderAll();
  });

  // >pager setup
  $('#pager').pagination({
    items: masterdata.length,
    itemsOnPage: pageLimit,
    cssStyle: 'light-theme',
    onPageClick: pagerdata,
    onInit: pagerdata
  });

  function pagerdata(pageNumber, event){
    if(!pageNumber){
      pageNumber = 1;
      fullDataTable
      .beginSlice(offset)
      .endSlice(offset+pageLimit);
      smallDataTable
      .beginSlice(offset)
      .endSlice(offset+pageLimit);
    }
    else{
      offset = pageNumber * pageLimit - pageLimit
      fullDataTable
      .beginSlice(offset)
      .endSlice(offset+pageLimit);
      smallDataTable
      .beginSlice(offset)
      .endSlice(offset+pageLimit);
    }  
    fullDataTable.redraw()
    smallDataTable.redraw()
  };

  if(allcomplete.value().total.issues == 0){
    $('#avg,#type-complete').empty().text('Sorry, there are currently no complete tickets to display.');
  }
});