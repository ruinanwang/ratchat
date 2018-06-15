
// site.js

// Function that makes scrolling smooth when clicking
// on anchor tages.
$(document).ready(function() {

  $("a").on('click', function(event) {

      if (this.hash !== "") {
        event.preventDefault();

        var hash = this.hash;

        $('html, body').animate({
          scrollTop: $(hash).offset().top
        }, 800, function(){

          window.location.hash = hash;
        });
      }
  });
});