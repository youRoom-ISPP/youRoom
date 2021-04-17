function coincidePass() {
    var pass = $("#password-reg").val();
    var confirmPass = $("#password-confirm-reg").val();
    if (pass != confirmPass) {
        $("#password-confirm-reg").css("background-color","#f8d7da");
        $("#boton-registro").attr("disabled", true);
    } else {
        $("#password-confirm-reg").css("background-color","#78f8da");
        if (pass.length > 7) {
            $("#boton-registro").attr("disabled", false);
        } else {
            $("#boton-registro").attr("disabled", true);
        }
    }
}

function longPass() {
    var pass = $("#password-reg").val();
    var confirmPass = $("#password-confirm-reg").val();
    if (pass.length < 8) {
        $("#password-reg").css("background-color","#f8d7da");
        $("#boton-registro").attr("disabled", true);
    } else {
        $("#password-reg").css("background-color","#78f8da");
        if (pass == confirmPass) {
            $("#boton-registro").attr("disabled", false);
        } else {
            $("#password-confirm-reg").css("background-color","#f8d7da");
        }
    }
}

$(document).ready(function(){
    $("#password-confirm-reg").keyup(coincidePass);
    $("#password-reg").keyup(longPass);
});