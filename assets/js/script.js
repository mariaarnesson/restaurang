$(".menu-toggle-btn").click(function(){
    $(this).toggleClass("fa-square-xmark");
    $(".navigation-menu").toggleClass("active");
  });




  var currentDateTime = new Date();
  var year = currentDateTime.getFullYear();
  var month = (currentDateTime.getMonth() + 1);
  var date = (currentDateTime.getDate() + 1);
  
  if(date < 10) {
    date = '0' + date;
  }
  if(month < 10) {
    month = '0' + month;
  }
  
  var dateTomorrow = year + "-" + month + "-" + date;
  var checkinElem = document.querySelector("#choose-date");
 
  
  checkinElem.setAttribute("min", dateTomorrow);
  
  checkinElem.onchange = function () {
      checkoutElem.setAttribute("min", this.value);
  }
