$(document).ready(function(){
	 $("div#homediv.add").hide();
  $("div#homediv").hover(function(event){
    this.style = "background-color:#0099ff;";
  },
  function(event){
	this.style = "background-color:;";
  });
  $("div#addlist").hover(function(event){
	  $(this).children(".add").show();
  },
  function(event){
	  $(this).children(".add").hide();
  }
  );
  $("#id_starttime").attr("type","datetime-local");
  $("#id_stoptime").attr("type","datetime-local");
});