$(function () {
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
      $(el).find('.add-activity-timetable-modal-trigger').removeClass('hide');
      $(el).find('.author-photo').addClass('hide');
    } else {
      $(el).addClass('panel-default');
      $(el).find(':checkbox').removeAttr('checked');
      $(el).find('.proposal-points').removeClass('hide');
      $(el).find('.proposal-timetable').addClass('hide');
      $(el).find('.add-activity-timetable-modal-trigger').addClass('hide');
      $(el).find('.author-photo').removeClass('hide');
    }
  });

  $(".add-activity-timetable-modal-trigger").click(function (e) {
    var modal = $('#add-activity-timetable-modal');
    $(modal).attr('data-href', $(this).attr('href'));
    $(modal).modal();
    e.preventDefault();
  });

  $('#add-activity-timetable-button').click(function () {
    var modal = $('#add-activity-timetable-modal');
    $.ajax({
      url: $(modal).attr('data-href'),
      method: 'POST',
      data: {
        start_timetable: $(modal).find('#id_start_timetable').val(),
        end_timetable: $(modal).find('#id_end_timetable').val(),
      }
    }).success(function(data, status, xhr) {
      var activityBlock = $('#' + data.slug);
      $(activityBlock).find('.proposal-points').addClass('hide');
      $(activityBlock).find('.proposal-timetable h3').text(data.timetable);
      $(activityBlock).find('.proposal-timetable').removeClass('hide');
      $(modal).modal('hide');
    });
  });

  $(".remove-activity").click(function () {
    $(this).parents('.proposal-item').remove();
  });
});