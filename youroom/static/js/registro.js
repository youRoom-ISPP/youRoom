//Comprobar que la contraseña es la misma
function coincidePass() {
    var pass = $("#password-reg").val();
    var confirmPass = $("#password-confirm-reg").val();
    if (pass != confirmPass) {
        $("#password-confirm-reg").css("background-color","#f8d7da");
        $("#boton-registro").attr("disabled", true);
    } else {
        $("#password-confirm-reg").css("background-color","#78f8da");
        $("#boton-registro").attr("disabled", false);
    }
}

//Comprobar que la contraseña tenga más de 8 caracteres
function longPass() {
    var pass = $("#password-reg").val();
    if (pass.length < 8) {
        $("#password-reg").css("background-color","#f8d7da");
        $("#boton-registro").attr("disabled", true);
    } else {
        $("#password-reg").css("background-color","#78f8da");
        if ($("#password-confirm-reg").val().length != 0) {
            $("#boton-registro").attr("disabled", false);
        }
    }
}

$(document).ready(function(){
    $("#password-confirm-reg").keyup(coincidePass);
    $("#password-reg").keyup(longPass);
});