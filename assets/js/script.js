$(".menu-toggle-btn").click(function(){
    $(this).toggleClass("fa-square-xmark");
    $(".navigation-menu").toggleClass("active");
  });




function draw() {
    var canvas = document.getElementById("myCanvas");
    var contex = canvas.getContext("2d");
    context.strokeSryle = "red";
    context.fillStyle = "rgba(0, 0, 255, 0.5)";
    context.fillRect(10,10,100,100);
    context.strokeRect(10,10,100,100);
}
