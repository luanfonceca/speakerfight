(function($) {
  $.fn.linkable = function() {
    return this.each(function() {
      $(this).css({cursor: 'pointer'});

      $(this).click(function (event) {
        event.preventDefault();
        window.location.replace(
          $(this).attr("data-href")
        );
      });
    });
  };
}(jQuery));