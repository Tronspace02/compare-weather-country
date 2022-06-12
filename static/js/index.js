$(".is-danger").on("click", function(){
    $("#imgDiv").remove();
    $("#obsTime").remove();
    window.location.href="/";
});

var sd=window.location.pathname;
if(sd=="/"){
    $("#imgDiv").remove();
    $("#obsTime").remove();
}