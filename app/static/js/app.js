
// app.js

// Function that makes scrolling smooth when clicking
// on page links.

$(document).ready(function() {

  $("a").on('click', function(event) {
      if (this.hash !== "") {
        event.preventDefault();

        var hash = this.hash;

        $('html, body').animate({
          scrollTop: $(hash).offset().top - 30
        }, 800, function(){
        });
      }
  });

  $('.carousel').carousel({interval: false});

});