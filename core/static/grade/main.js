$(document).ready(function(){
  $(".event").each(function(){
    
    var event = $(this);
    event.find(".long").hide();
    
    event.find(".more-button").on("click",function(e){
      console.log(e);
      e.preventDefault();
      event.find(".long").slideToggle();
    })   
    
  })

  $(".agenda .event .long").hide();

});