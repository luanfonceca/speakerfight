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

  $("#event-approved-proposals").sortable({
    stop: function (event, ui) {
      var activities = $("#event-approved-proposals").sortable("toArray");
      var serializedActivities = [];

      for (var i = 0; i < activities.length; i++) {
        serializedActivities.push({
          slug: activities[i],
          order: i
        });
      }

      $.ajax({
        url: $("#event-approved-proposals").attr('data-href'),
        method: 'PATCH',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
        data: {
          activities: JSON.stringify(serializedActivities)
        }
      }).error(function(data, status, xhr) {
        if (data.status == 403) {
          alert(data.responseJSON.detail);
        }

        for (field in data.responseJSON){
          $('[name="' + field + '"]').parents('.form-group').addClass('has-error');
        }
      });
    }
  });

  $("#event-approved-proposals").disableSelection();

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
      $(modal).find('#id_title').val(data.title);
      $(modal).find('#id_description').val(data.description);
      tinymce.get('id_description').setContent(data.description);
      $(modal).find('#id_start_timetable').val(data.start_timetable);
      $(modal).find('#id_end_timetable').val(data.end_timetable);
      $(modal).find('#oldSlug').val(data.slug);
    });

    $(modal).attr('data-href', $(this).parents('.panel').attr('data-href'));
    $(modal).modal();
  });

  $('.proposal-container').delegate('.update-proposal', 'click', function(e) {
    e.preventDefault();
    var modal = $('#update-proposal-modal');
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

  $('#update-proposal-form').submit(function (e) {
    e.preventDefault();
    var modal = $('#update-proposal-modal');

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
        title: $(modal).find('#id_title').val(),
        description: $(modal).find('#id_description').val(),
        start_timetable: $(modal).find('#id_start_timetable').val(),
        end_timetable: $(modal).find('#id_end_timetable').val(),
      }
    }).success(function(data, status, xhr) {

      var oldSlug = $(modal).find('#oldSlug').val();

      $(modal).attr('data-href', data.url_api_event_activity)
      $('#' + oldSlug).attr('data-href', data.url_api_event_activity);
      $('#' + oldSlug).attr('id', data.slug);

      var activityBlock = $('#' + data.slug);
      $(activityBlock).find('.proposal-points').addClass('hide');
      $(activityBlock).find('.proposal-timetable .timetable').text(data.timetable);
      $(activityBlock).find('.proposal-title a').text(data.title);
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

  $(".proposal-actions").on('click', '.approve-link', function(e) {
    e.preventDefault();
    var self = $(this);
    if (!self.attr('href')) {
      return;
    }

    $.ajax({
      url: self.attr('href'),
      method: 'POST'
    }).success(function(data, status, xhr) {
      var old_href = self.attr('href');
      var new_href = old_href.replace('/approve_proposal', '/disapprove_proposal');
      self.attr('href', new_href);
      var old_title = self.attr('data-original-title');
      var new_title = old_title.replace(
        gettext('Approve the proposal.'), gettext('Disapprove the proposal.'));
      self.attr('data-original-title', new_title);
      self.removeClass('approve-link');
      self.addClass('disapprove-link');
      self.find('i').attr('class', 'icon-check-empty');
      self.find('span').html(gettext('Disapprove'));
      self.blur();
      self.parents('.proposal-item').find('.update-activity').removeClass('hide');

      // move to approved list
      self.parents('.proposal-item').appendTo("#event-approved-proposals");

      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-approved-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                             data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      $('#message').append(successAlert);
      window.setTimeout(function() {
        $("#succes-approved-alert").alert('close');
      }, 3000);
    }).error(function(xhr, status, error) {
      if (xhr.responseJSON) {
        if (xhr.responseJSON.redirectUrl) {
          window.location.href = xhr.responseJSON.redirectUrl;
        } else if (xhr.responseJSON.message) {
          var errorAlert = '<div class="alert alert-danger alert-dismissable text-left">' +
                             '<i class="icon-exclamation-sign"></i>' +
                               xhr.responseJSON.message +
                             '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                           '</div>';
          $('#message').append(errorAlert);
        }
      }
    });
  });


  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

  $(".proposal-actions").on('click', '.disapprove-link', function(e) {
    e.preventDefault();
    var self = $(this);
    if (!self.attr('href')) {
      return;
    }

    $.ajax({
      url: self.attr('href'),
      method: 'POST'
    }).success(function(data, status, xhr) {
      var old_href = self.attr('href');
      var new_href = old_href.replace('/disapprove_proposal', '/approve_proposal');
      self.attr('href', new_href);
      var old_title = self.attr('data-original-title');
      var new_title = old_title.replace(
        gettext('Disapprove the proposal.'), gettext('Approve the proposal.'));
      self.attr('data-original-title', new_title);
      self.removeClass('disapprove-link');
      self.addClass('approve-link');
      self.find('i').attr('class', 'icon-check');
      self.find('span').html(gettext('Approve'));
      self.blur();
      self.parents('.proposal-item').find('.update-activity').addClass('hide');

      self.parents('.proposal-item').appendTo("#event-not-approved-proposals");

      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-disapproved-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                             data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      $('#message').append(successAlert);
      window.setTimeout(function() {
        $("#succes-disapproved-alert").alert('close');
      }, 3000);
    }).error(function(xhr, status, error) {
      if (xhr.responseJSON) {
        if (xhr.responseJSON.redirectUrl) {
          window.location.href = xhr.responseJSON.redirectUrl;
        } else if (xhr.responseJSON.message) {
          var errorAlert = '<div class="alert alert-danger alert-dismissable text-left">' +
                             '<i class="icon-exclamation-sign"></i>' +
                               xhr.responseJSON.message +
                             '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                           '</div>';
          $('#message').append(errorAlert);
        }
      }
    });
  });

  tinymce.init({
    selector: "[name='description']",
    menubar: false,
    skin: 'light',
    plugins: 'link paste preview textcolor',
    toolbar: "bold italic underline forecolor | alignleft aligncenter alignright | link unlink | undo redo removeformat | formatselect fontsizeselect pastetext | preview",
    body_class: 'form-control',
  });
});
