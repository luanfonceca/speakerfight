$(function () {
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

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

  $(".proposal-votes").on('click', '.voting-link', function(e) {
    e.preventDefault();
    var self = $(this);
    if (!self.attr('href')) {
      return;
    }

    $.ajax({
      url: self.attr('href'),
      method: 'POST'
    }).success(function(data, status, xhr) {
      // Make previous vote link clickable and current vote not clickable!
      unvote = self.parent('.proposal-votes').find('.no-hover');
      self.add(unvote).toggleClass('no-hover voting-link');
      unvote.attr('href', unvote.attr('data-href'))
            .removeAttr('data-href');
      self.attr('data-href', self.attr('href'))
          .removeAttr('href');
      // Display success message
      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-vote-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                             data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      self.parent('.proposal-votes').parent('.panel-body').append(successAlert);
      window.setTimeout(function() {
        $("#succes-vote-alert").alert('close');
      }, 3000);
    }).error(function(xhr, status, error) {
      if (xhr.responseJSON) {
        if (xhr.responseJSON.redirectUrl) {
          window.location.href = xhr.responseJSON.redirectUrl;
        } else if (xhr.responseJSON.message) {
          var errorAlert = '<div class="alert alert-danger alert-dismissable text-left id="error-vote-alert"">' +
                             '<i class="icon-exclamation-sign"></i>' +
                               xhr.responseJSON.message +
                             '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                           '</div>';
          self.parent('.proposal-votes').parent('.panel-body').append(errorAlert);
        }
      }
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

      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-approved-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                             data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      self.parents('.proposal-item').find('.proposal-votes').append(successAlert);
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
          self.parents('.proposal-item').find('.proposal-votes').append(errorAlert);
        }
      }
    });
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

      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-disapproved-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                             data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      self.parents('.proposal-item').find('.proposal-votes').append(successAlert);
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
          self.parents('.proposal-item').find('.proposal-votes').append(errorAlert);
        }
      }
    });
  });
});
