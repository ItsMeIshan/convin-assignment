function calendarAuthenticate() {
  $.ajax({
    type: "GET",
    url: "ajax/init",
    // data: '',
    success: function (data) {
      console.log("Done");
    },
  });
}
