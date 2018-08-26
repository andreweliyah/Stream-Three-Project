'use strict';

d3.json('/api-tracker/ticket/').then(function(masterdata){ 
  console.log(masterdata)
  var truncate = 20
  if(masterdata.length!==0){
    // fix color scheme error
    dc.config.defaultColors(d3.schemeSet1)
   
    // function to reformat data
    function formatData(masterdata) {
      var dateFormatSpecifier = '%Y-%m-%d';
      var dateFormat = d3.timeFormat(dateFormatSpecifier);
      var dateFormatParser = d3.timeParse(dateFormatSpecifier)

      masterdata.forEach(function(d,i){
        
        if(masterdata[i].description.length>truncate)
        {
          masterdata[i].description = masterdata[i].description.substring(0,truncate)+' ...';
        }
        masterdata[i].modified = dateFormatParser(masterdata[i].modified);
        masterdata[i].link = '<a href="/tracker/ticket-'+masterdata[i].id+'/">Go to Ticket</a>';
      });
      return masterdata
    }
    

    // >formated data for all tickets
    masterdata = formatData(masterdata);
    
    // >data for active tickets
    var active = [];
    var activeBugs = [];
    var activeFeatures = [];
    var completeTickets = [];

    // seperate the data by type and filter by status
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
    console.log(activeFeatures)
    // sort data by votes
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

    // reverse sorted data so it flows in descending order
    activeFeatures.reverse();
    activeBugs.reverse();

    // save only the top 5 tickets and trash the rest
    activeBugs.splice(4,activeBugs.length-5)
    activeFeatures.splice(4,activeFeatures.length-5)

    // >averages section
    if(completeTickets.length != 0){
      var ndx = crossfilter(completeTickets);
      var all = ndx.groupAll().reduce(reduce.add,reduce.remove,reduce.init);
      var dayAvg = dc.numberDisplay('#day-avg');
      dayAvg
        .group(all)
        .formatNumber(d3.format(".1s"))
        .valueAccessor(function(d) {
          return d.total.issues/d.total.days;
         })
        .html({
                one:"<span>%number</span> ticket a day",
                some:"<span>%number</span> tickets a day",
                none:"<span>no</span> tickets whatsoever"
              })

      var weekAvg = dc.numberDisplay('#week-avg');
      weekAvg
        .group(all)
        .formatNumber(d3.format(".1s"))
        .valueAccessor(function(d) {
          return d.total.issues/d.total.weeks;
         })
        .html({
                one:"<span>%number</span> ticket a week",
                some:"<span>%number</span> tickets a week",
                none:"<span>no</span> tickets at all"
              })

      var monthAvg = dc.numberDisplay('#month-avg');
      monthAvg
        .group(all)
        .formatNumber(d3.format(".1s"))
        .valueAccessor(function(d) {
          return d.total.issues/d.total.months;
         })
        .html({
                one:"<span>%number</span> ticket a month",
                some:"<span>%number</span> tickets a month",
                none:"<span>0</span> tickets period"
              })

      // >percent of complete tickets by type
      var featureByStatus = ndx.dimension(dc.pluck('type'))
      var featureGroup = featureByStatus.group()
      
      var typeComplete = dc.pieChart('#type-complete');
      
      typeComplete
        .dimension(featureByStatus)
        .group(featureGroup)
        .label(function (d) {
          return d.key+': '+Math.floor(d.value*100/completeTickets.length)+'%'
        })
        .filter = function() {};
    }
    else{
      $('#type-complete,#avg').hide();
    }
     

    // >top 5 voted features
    if(activeFeatures.length != 0){
      var ndx2 = crossfilter(activeFeatures);
      var ticketsByTypeFeature = ndx2.dimension(dc.pluck('type'));
      ticketsByTypeFeature.filter('FEATURE');
      var featureVoteChart = dc.dataTable('#vote-feature');
      featureVoteChart
      .dimension(ticketsByTypeFeature)
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
    }
    else{
      $('#vote-feature').text('There are currently no active features')
    }
      

    if(activeBugs.length != 0){
      // >top 5 voted bugs
      var ndx3 = crossfilter(activeBugs);
      var ticketsByTypeBug = ndx3.dimension(dc.pluck('type'));
      ticketsByTypeBug.filter('BUG');
      var bugVoteChart = dc.dataTable('#vote-bug');
      bugVoteChart
      .dimension(ticketsByTypeBug)
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
    }
    else{
      $('#vote-bug').text('There are currently no active bugs')
    } 


    
    dc.renderAll();
  }
  else{
    $('main').html('<h2>No Data Avaiable</h2>');
  }
});