
// app.js

$(document).ready(function () {
  // Smooth scrolling function
  $("a").on('click', function (event) {
    if (this.hash !== "") {
      event.preventDefault();

      var hash = this.hash;

      $('html, body').animate({
        scrollTop: $(hash).offset().top - 30
      }, 800, function () {});
    }
  });

  // Setting click listeners for side navigation
  $("#menu").on('click', function () {
    openNav();
  });
  
  $("#overlay").on('click', function() {
    closeNav();
  });
});

// Functions for handling side navigation appearance
function openNav() {
  document.getElementById("sidebar").style.width = "200px";
  document.getElementById("wrapper").style.marginRight = "200px";
  document.getElementById("wrapper").style.marginLeft = "-200px";
  document.getElementById("overlay").style.marginRight = "200px";
  document.getElementById("overlay").style.marginLeft = "-200px";
  document.getElementById("overlay").style.zIndex = "999";
}

function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("wrapper").style.marginRight = "0";
  document.getElementById("wrapper").style.marginLeft = "0";
  document.getElementById("overlay").style.marginRight = "0";
  document.getElementById("overlay").style.marginLeft = "0";
  document.getElementById("overlay").style.zIndex = "-999";
}

// Merge Sort Functions
function mergeSort(arr) {
  if (arr.length === 1) {
    return arr
  }

  const middle = Math.floor(arr.length / 2)
  const left = arr.slice(0, middle)
  const right = arr.slice(middle)

  return merge(
    mergeSort(left),
    mergeSort(right)
  )
}

function merge(left, right) {
  let result = []
  let indexLeft = 0
  let indexRight = 0

  while (indexLeft < left.length && indexRight < right.length) {
    if (left[indexLeft]['time'] < right[indexRight]['time']) {
      result.push(left[indexLeft])
      indexLeft++
    } else {
      result.push(right[indexRight])
      indexRight++
    }
  }

  return result.concat(left.slice(indexLeft)).concat(right.slice(indexRight))
}