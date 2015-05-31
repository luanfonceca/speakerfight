(function($) {
  $.fn.linkable = function() {
    return this.each(function() {
      $(this).css({cursor: 'pointer'});

      $(this).click(function (event) {
        if (!event.target.href) {
          event.preventDefault();
          window.location.replace(
            $(this).attr("data-href")
          );
        }
      });
    });
  };
}(jQuery));