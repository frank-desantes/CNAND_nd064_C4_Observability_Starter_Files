$(document).ready(function () {

    // all custom jQuery will go here
    $("#firstbutton").click(function () {
        $.ajax({
            // url: "http://backend-service.default.svc.cluster.local", success: function (result) {
            url: "http://localhost:8081/api", success: function (result) {
                $("#firstbutton").toggleClass("btn-primary:focus");
                }
        });
    });
    $("#secondbutton").click(function () {
        $.ajax({
            // url: "http://trial-service.default.svc.cluster.local", success: function (result) {
            url: "http://localhost:8082", success: function (result) {
                $("#secondbutton").toggleClass("btn-primary:focus");
            }
        });
    });    
});