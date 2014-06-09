(function($) {
  $.fn.linkable = function() {
    return this.each(function() {
      $(this).css({cursor: 'pointer'});

      $(this).click(function () {
        window.location.replace(
          $(this).attr("data-href")
        );
      });
    });
  };
}(jQuery));