$(function () {
  $(".voting-link").on('click', function(e) {
    e.preventDefault();
    var $me = $(this);
    if (!$me.attr('href')) {
      return;
    }

    $.ajax({
      url: $me.attr('href'),
      method: 'POST'
    })
    .success(function(data, status, xhr) {
      $me.parent('.proposal-votes').find('.voting-link').not($me).remove();
      $me.attr('href', '');
      var successAlert = '<div class="alert alert-success alert-dismissable" id="succes-vote-alert">' +
                          '<i class="icon-exclamation-sign"></i>' + data.message +
                          '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                        '</div>';
      $me.parent('.proposal-votes').append(successAlert);
      window.setTimeout(function() {
        $("#succes-vote-alert").alert('close');
      }, 3000);
    })
    .error(function(xhr, status, error) {
      if (xhr.responseJSON) {
        if (xhr.responseJSON.redirectUrl) {
          window.location.href = xhr.responseJSON.redirectUrl;
        } else if (xhr.responseJSON.errorMessage) {
          var errorAlert = '<div class="alert alert-danger alert-dismissable">' +
                              '<i class="icon-exclamation-sign"></i>' +
                              xhr.responseJSON.errorMessage +
                              '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
                            '</div>';
          $me.parent('.proposal-votes').append(errorAlert);
        }
      }
    });
  });
});
