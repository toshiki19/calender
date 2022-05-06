document.addEventListener('DOMContentLoaded', function() {
  console.log(events)
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      
        eventClick: function (info) {
        // console.log('ここから')
        // console.log(info)
        var start = info.el.fcSeg.eventRange.range.start
        var end = info.el.fcSeg.eventRange.range.end 
        console.log(start)
        console.log(end)
        const event = info.event;
        var YYYY = start.getFullYear();
        var MM = start.getMonth()+1;
        var DD = start.getDate();
        var a = start.getHours();
        var b = start.getMinutes();
        if (MM < 10) {
          MM = "0" + MM
        }
        if (DD < 10) {
          DD = "0" + DD
        }
        if (a < 10) {
          a = "0" + a
        }
        if (b < 10) {
          b = "0" + b
        }
        var YYY2 = end.getFullYear();
        var M2 = end.getMonth()+1;
        var D2 = end.getDate();
        var c = end.getHours();
        var d = end.getMinutes();
        if (M2 < 10) {
          M2 = "0" + M2
        }
        if (D2 < 10) {
          D2 = "0" + D2
        }
        if (c < 10) {
          c = "0" + c
        }
        if (d < 10) {
          d = "0" + d
        }
        $('#calender_change-form #start').val(YYYY + "-" + MM + "=" + DD + "T" + a + ":" + b)
        $('#calender_change-form #end').val(YYY2 + "-" + M2 + "=" + D2 + "T" + c + ":" + d)
        $('#calender_change-form #title').val(event.title)
        $('#calender_change-form #body').val(event.extendedProps.body)
        $('#calender_change-form #id').val(event.id)
        $('#calender_change-form').show();
    },
      dateClick: function(info) {
        console.log(info)
        // $('#calender-form #color').val(info.bgColor) 
        $('#calender-form #dates').val(info.dateStr)
        $('#calender-form #title').val(info.title)
        $('#calender-form #body').val(info.body)
        $('#calender-form').show();
    },
    
      locale: 'ja',
                buttonText: {
                    prev:     '<',
                    next:     '>',
                    prevYear: '<<',
                    nextYear: '>>',
                    today:    '今日',
                    month:    '月',
                    week:     '週',
                    day:      '日',
                    list:     '一覧'
                },
      navLinks: true,
      businessHours: true,
      editable: true,
      dayMaxEvents: true,
      
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'title',
        center: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
        right: 'prev,today,next'
        },
        eventSources: [
          {
            googleCalendarApiKey: 'AIzaSyBPN9zW60xSDcBKJ0rxh6b60lH53wgSy4w',
            googleCalendarId: 'japanese__ja@holiday.calendar.google.com',
            display: 'background',
            color:"#ffd0d0"
          }
        ],
        eventDurationEditable : false,
        events: '/hoge/list',
      events:events,
              
    });
    
    calendar.render();
    
    $('#close-btn').on('click', function () {
        $('#calender-form').find("textarea, :text, select").val("").end().find(":checked").prop("checked", false);
        $('#calender-form').hide();
    });

    $('#close-btn2').on('click', function () {
      $('#calender_change-form').find("textarea, :text, select").val("").end().find(":checked").prop("checked", false);
      $('#calender_change-form').hide();
  });

  });
  
  // function getjson() {
  //   let xhr = new XMLHttpRequest();
  //   xhr.open('GET', 'https://jsonplaceholder.typicode.com/todos');
  //   xhr.onload = function () {
  //   if (xhr.readyState == 4 && xhr.status == 200) {
  //   console.log(xhr.responseText);
  //   } else {
  //   console.log("status = " + status.status);
  //   }
  //   }
  //   xhr.send();
  //   }
  //   getjson();
