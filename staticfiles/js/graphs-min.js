"use strict";d3.json("/api-tracker/ticket/").then(function(e){function t(e,t){var n="%Y-%m-%d",i=d3.timeFormat("%Y-%m-%d"),o=d3.timeParse("%Y-%m-%d");return e.forEach(function(n,i){e[i].description.length>t&&(e[i].description=e[i].description.substring(0,t)+" ..."),e[i].modified=o(e[i].modified),e[i].link='<a href="/tracker/ticket-'+e[i].id+'/">Go to Ticket</a>'}),e}function n(e,t){e?(o=e*s-s,f.beginSlice(o).endSlice(o+s),g.beginSlice(o).endSlice(o+s)):(e=1,f.beginSlice(o).endSlice(o+s),g.beginSlice(o).endSlice(o+s)),f.redraw(),g.redraw()}dc.config.defaultColors(d3.schemeSet1);var i={add:function(e,t,n){e.total.issues++,e.days[t.modified]?e.days[t.modified]++:(e.days[t.modified]=1,e.total.days++);var i=t.modified.getDate()-t.modified.getDay();i=new Date(t.modified.getFullYear(),t.modified.getMonth(),i);var o=i.getDate()+6;return o=new Date(t.modified.getFullYear(),t.modified.getMonth(),o),e.weeks[i+""+o]?e.weeks[i+""+o]++:(e.weeks[i+""+o]=1,e.total.weeks++),i=new Date(t.modified.getFullYear(),t.modified.getMonth(),1),o=new Date(t.modified.getFullYear(),t.modified.getMonth()+1,1),e.months[i+""+o]?e.months[i+""+o]++:(e.months[i+""+o]=1,e.total.months++),e},remove:function(e,t,n){e.total.issues--,e.days[t.modified]?e.days[t.modified]--:e.total.days--;var i=t.modified.getDate()-t.modified.getDay();i=new Date(t.modified.getFullYear(),t.modified.getMonth(),i);var o=i.getDate()+6;return o=new Date(t.modified.getFullYear(),t.modified.getMonth(),o),e.weeks[i+""+o]?e.weeks[i+""+o]--:e.total.weeks--,i=new Date(t.modified.getFullYear(),t.modified.getMonth(),1),o=new Date(t.modified.getFullYear(),t.modified.getMonth()+1,1),e.months[i+""+o]?e.months[i+""+o]--:e.total.months--,e},init:function(){return{total:{issues:0,days:0,weeks:0,months:0},days:{},weeks:{},months:{}}}},o=0,s=10,d=20,r=[],a=[],l=[],c=[],u=dc.numberDisplay("#number"),m=dc.selectMenu("#status-select"),p=dc.selectMenu("#type-select"),f=dc.dataTable("#fulllist"),g=dc.dataTable("#smalllist"),h=dc.textFilterWidget("#id-field"),k=dc.textFilterWidget("#search-field"),y=dc.numberDisplay("#day-avg"),v=dc.numberDisplay("#week-avg"),b=dc.numberDisplay("#month-avg"),w=dc.pieChart("#type-complete"),D=dc.dataTable("#vote-feature"),S=dc.dataTable("#vote-feature-small"),T=dc.dataTable("#vote-bug"),F=dc.dataTable("#vote-bug-small"),A=t(e,20),M=crossfilter(A),Y,O,P,N=M.groupAll(),z,B=M.dimension(dc.pluck("type")),E=M.dimension(dc.pluck("id")),G=M.dimension(dc.pluck("status")),I=M.dimension(dc.pluck("description")),C,U,W,x=B.group(),j=G.group(),H=I.group(),R;A.forEach(function(e){"TODO"==e.status||"DOING"==e.status?"BUG"==e.type?a.push(e):l.push(e):c.push(e),"DONE"!=e.status&&"DOING"!=e.status||r.push(e)}),l.sort(function(e,t){return e.votes>t.votes?1:e.votes<t.votes?-1:0}),a.sort(function(e,t){return e.votes>t.votes?1:e.votes<t.votes?-1:0}),a.splice(4,a.length-5),l.splice(4,l.length-5),l.reverse(),a.reverse(),Y=crossfilter(c),O=crossfilter(l),P=crossfilter(a),z=Y.groupAll().reduce(i.add,i.remove,i.init),C=Y.dimension(dc.pluck("type")),U=O.dimension(dc.pluck("type")),W=P.dimension(dc.pluck("type")),R=C.group(),U.filter("FEATURE"),W.filter("BUG"),y.group(z).formatNumber(d3.format(".1s")).valueAccessor(function(e){return e.total.issues/e.total.days}).html({one:"<span>%number</span> ticket a day",some:"<span>%number</span> tickets a day",none:"<span>no</span> tickets whatsoever"}),v.group(z).formatNumber(d3.format(".1s")).valueAccessor(function(e){return e.total.issues/e.total.weeks}).html({one:"<span>%number</span> ticket a week",some:"<span>%number</span> tickets a week",none:"<span>no</span> tickets at all"}),b.group(z).formatNumber(d3.format(".1s")).valueAccessor(function(e){return e.total.issues/e.total.months}).html({one:"<span>%number</span> ticket a month",some:"<span>%number</span> tickets a month",none:"<span>0</span> tickets period"}),w.dimension(C).minWidth(100).group(R).label(function(e){return e.key+": "+Math.floor(100*e.value/c.length)+"%"}),h.dimension(E).normalize(function(e){return e.toString()}).placeHolder("Enter ID"),p.dimension(B).group(x),m.dimension(G).group(j),k.dimension(I),f.dimension(E).group(function(e){return"All"}).columns(["id","type","status","description","votes","link"]),g.dimension(E).group(function(e){return"All"}).columns(["type","description","link"]),D.dimension(U).group(function(e){return"TOP 5 "+e.type+"S"}).columns(["id","status","description","votes","link"]).sortBy(function(e){return e.votes}).order(d3.descending).size(5),S.dimension(U).group(function(e){return"TOP 5 "+e.type+"S"}).columns(["type","description","link"]).sortBy(function(e){return e.votes}).order(d3.descending).size(5),T.dimension(W).group(function(e){return"TOP 5 "+e.type+"S"}).columns(["id","status","description","votes","link"]).sortBy(function(e){return e.votes}).order(d3.descending).size(5),F.dimension(W).group(function(e){return"TOP 5 "+e.type+"S"}).columns(["type","description","link"]).sortBy(function(e){return e.votes}).order(d3.descending).size(5),u.group(N).formatNumber(d3.format("")).valueAccessor(function(e){return f.beginSlice(0).endSlice(s),g.beginSlice(0).endSlice(s),$(function(){$("#pager").pagination("updateItems",e),$("#pager").pagination("selectPage",1),f.beginSlice(0).endSlice(s),g.beginSlice(0).endSlice(s)}),e}).html({one:"<span>%number</span> ticket",some:"<span>%number</span> tickets",none:"<span>0</span> tickets"}),dc.renderAll(),$(window).resize(function(){dc.renderAll()}),$("#pager").pagination({items:A.length,itemsOnPage:s,cssStyle:"light-theme",onPageClick:n,onInit:n})});