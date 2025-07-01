// Set the time limit in seconds
var timeLimit = 60;

// Get the timer element from the DOM
var timer = document.getElementById('countdown-timer');

// Start the countdown timer
var interval = setInterval(function() {
  // Decrement the time limit by 1 second
  timeLimit--;

  // Calculate the minutes and seconds remaining
  var minutes = Math.floor(timeLimit / 60);
  var seconds = timeLimit % 60;

  // Add leading zeros to the minutes and seconds if necessary
  minutes = (minutes < 10 ? '0' : '') + minutes;
  seconds = (seconds < 10 ? '0' : '') + seconds;

  // Update the timer element with the new time
  timer.innerHTML = minutes + ':' + seconds;

  // If the time limit has been reached, stop the timer
  if (timeLimit <= 0) {
    clearInterval(interval);
    timer.innerHTML = 'Time expired';
  }
}, 1000);



function countdown(minutes, seconds) {
  console.log("countdown function called");
  var timerElement = document.getElementById("countdown-timer");

  var intervalId = setInterval(function() {
    console.log("interval function called");
    if (seconds == 0) {
      if (minutes == 0) {
        clearInterval(intervalId);
        timerElement.innerHTML = "Time's up!";
      } else {
        minutes--;
        seconds = 59;
      }
    } else {
      seconds--;
    }
    console.log("minutes:", minutes, "seconds:", seconds);
    timerElement.innerHTML = minutes.toString() + ":" + (seconds < 10 ? "0" : "") + seconds.toString();
  }, 1000);
}

countdown(1, 0);