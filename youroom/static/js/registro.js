function compruebaPass() {
    var pass = $("#password-reg").val();
    var confirmPass = $("#password-confirm-reg").val();
    $("#boton-registro").attr("disabled", true);
    if (pass.length > 7 && pass == confirmPass) {
        $("#password-reg").css("background-color","#78f8da");
        $("#password-confirm-reg").css("background-color","#78f8da");
        $("#boton-registro").attr("disabled", false);
    } else {
        if (pass.length > 7) {
            $("#password-reg").css("background-color","#78f8da");
            $("#password-confirm-reg").css("background-color","#f8d7da");
        } else if (pass == confirmPass) {
            $("#password-confirm-reg").css("background-color","#78f8da");
            $("#password-reg").css("background-color","#f8d7da");
        } else {
            $("#password-reg").css("background-color","#f8d7da");
            $("#password-confirm-reg").css("background-color","#f8d7da");
        }
        $("#boton-registro").attr("disabled", true);
    }
}

$(document).ready(function(){
    $("#password-confirm-reg").keyup(compruebaPass);
    $("#password-reg").keyup(compruebaPass);
});