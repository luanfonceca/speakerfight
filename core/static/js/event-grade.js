$(function () {
  // using jQuery
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  dragula([
    $('#event-approved-proposals')[0],
    $('#event-not-approved-proposals')[0],
    $('#event-activities')[0],
  ], {
    accepts: function (el, target, source, sibling) {
      var isNotApprovedContainer = $(target).attr('id') == 'event-not-approved-proposals';
      var isEventActivityItem = $(el).hasClass('event-activity');
      if (isNotApprovedContainer && isEventActivityItem) {
        return false;
      }
      return true;
    }
  }).on('drop', function (el, container, source) {
    if (source == container) {
      return;
    }
    $(el).removeClass('panel-success panel-warning panel-default');
    
    if ($(container).attr('id') == 'event-approved-proposals') {
      $(el).addClass('panel-success');
      $(el).find(':checkbox').attr('checked', 'checked');
      $(el).find('.proposal-points').addClass('hide');
      $(el).find('.proposal-timetable').removeClass('hide');
      $(el).find('.update-activity').removeClass('hide');
      $(el).find('.author-photo').addClass('hide');
    } else {
      $(el).addClass('panel-default');
      $(el).find(':checkbox').removeAttr('checked');
      $(el).find('.proposal-points').removeClass('hide');
      $(el).find('.proposal-timetable').addClass('hide');
      $(el).find('.update-activity').addClass('hide');
      $(el).find('.author-photo').removeClass('hide');
    }
  });

  $('#add-activity-form').submit(function (e) {
    e.preventDefault();
    var modal = $('#add-activity-modal');

    $.ajax({
      url: $(modal).attr('data-href'),
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      data: {
        title: $(modal).find('#id_title').val(),
        description: $(modal).find('#id_description').val(),
        activity_type: $(modal).find('#id_activity_type').val(),
        start_timetable: $(modal).find('#id_start_timetable').val(),
        end_timetable: $(modal).find('#id_end_timetable').val(),
      }
    }).success(function(data, status, xhr) {
      var activityItem = ''+
        '<div id="' + data.slug + '" data-href="' + data.url_api_event_activity + '" class="panel panel-success proposal-item event-activity">'+
          '<div class="panel-body">'+
            '<input checked="checked" name="approved_activities" value="' + data.pk + '" class="hide" type="checkbox" />'+
            '<div class="pull-right proposal-actions">'+
              '<button type="button" class="btn-flat gray text-upper update-activity">'+
                '<i class="icon-pencil"></i>'+
              '</button>'+
              '&nbsp;'+
              '<button type="button" class="btn-flat gray text-upper remove-activity">'+
                '<i class="icon-trash"></i>'+
              '</button>'+
            '</div>'+
            '<div class="pull-left text-center proposal-rate">'+
              '<div class="proposal-timetable">'+
                '<p>' + data.activity_type_display + '</p>'+
                '<span class="timetable">' + data.timetable + '</span class="timetable">'+
              '</div>'+
            '</div>'+
            '<div>'+
              '<h3 class="panel-title proposal-title">'+
                '<a href="#' + data.slug + '">' + data.title + '</a>'+
                '<p class="proposal-metadata">' + data.description + '</p>'+
              '</h3>'+
            '</div>'+
          '</div>'+
        '</div>';
      $("#event-approved-proposals").prepend(activityItem);
      $(modal).modal('hide');
    }).error(function(data, status, xhr) {
      if (data.status == 403) {
        alert(data.responseJSON.detail)
      };
      for (field in data.responseJSON){
        $('[name="' + field + '"]').parents('.form-group').addClass('has-error');
      }
    });
  });

  $('.proposal-container').delegate('.update-activity', 'click', function(e) {
    e.preventDefault();
    var modal = $('#update-activity-modal');
    $.ajax({
      url: $(this).parents('.panel').attr('data-href'),
      method: 'GET',
    }).success(function(data, status, xhr) {
      $(modal).find('#id_start_timetable').val(data.start_timetable);
      $(modal).find('#id_end_timetable').val(data.end_timetable);
    });

    $(modal).attr('data-href', $(this).parents('.panel').attr('data-href'));
    $(modal).modal();
  });

  $('#update-activity-form').submit(function (e) {
    e.preventDefault();
    var modal = $('#update-activity-modal');

    $.ajax({
      url: $(modal).attr('data-href'),
      method: 'PATCH',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      data: {
        start_timetable: $(modal).find('#id_start_timetable').val(),
        end_timetable: $(modal).find('#id_end_timetable').val(),
      }
    }).success(function(data, status, xhr) {
      var activityBlock = $('#' + data.slug);
      $(activityBlock).find('.proposal-points').addClass('hide');
      $(activityBlock).find('.proposal-timetable .timetable').text(data.timetable);
      $(activityBlock).find('.proposal-timetable').removeClass('hide');
      $(modal).modal('hide');
    }).error(function(data, status, xhr) {
      if (data.status == 403) {
        alert(data.responseJSON.detail)
      };
      for (field in data.responseJSON){
        $('[name="' + field + '"]').parents('.form-group').addClass('has-error');
      }
    });
  });

  $('.proposal-container').delegate('.remove-activity', 'click', function(e) {
    e.preventDefault();
    var self = this;

    var message = gettext('Are you sure you want to remove this activity?');
    if (!confirm(message)) {
      return false;
    }

    $.ajax({
      url: $(this).parents('.panel').attr('data-href'),
      type: 'DELETE',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      },
      success: function(result) {
        $(self).parents('.proposal-item').remove();
      }
    }).error(function(data, status, xhr) {
      if (data.status == 403) {
        alert(data.responseJSON.detail)
      };
    });
  });
});