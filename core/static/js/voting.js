$(function () {
  $(".voting-link").on('click', function(e) {
    e.preventDefault();
    var self = $(this);
    if (!self.attr('href')) {
      return;
    }

    $.ajax({
      url: self.attr('href'),
      method: 'POST'
    }).success(function(data, status, xhr) {
      self.parent('.proposal-votes').find('.voting-link').not(self).remove();
      self.removeAttr('href');
      var successAlert = '<div class="alert alert-success alert-dismissable text-left" id="succes-vote-alert">' +
                           '<i class="icon-exclamation-sign"></i>' +
                           data.message +
                           '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                         '</div>';
      self.parent('.proposal-votes').append(successAlert);
      window.setTimeout(function() {
        $("#succes-vote-alert").alert('close');
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
          self.parent('.proposal-votes').append(errorAlert);
        }
      }
    });
  });
});
