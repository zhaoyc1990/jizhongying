$(document).ready(function(){

    var isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i) ? true: false;
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i) ? true: false;
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i) ? true: false;
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i) ? true: false;
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());
        }
    };
    var mobileclickcontrol = true;
    if (isMobile.any()){
        $("div#addlist").click(function(event){
            if (mobileclickcontrol){
                mobileclickcontrol = false
                $(this).children(".add").hide();
            }else{
                mobileclickcontrol = true
                $(this).children(".add").show();
            }

        });

    }else{
          $("div#addlist").hover(function(event){
          $(this).children(".add").show();
            },
            function(event){
            $(this).children(".add").hide();
        });
    }
    $("div#homediv.add").hide();
    $("div#homediv").hover(function(event){
    this.style = "background-color:#0099ff;";
    },
    function(event){
    this.style = "background-color:;";
    });


});