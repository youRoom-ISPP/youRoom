//Comprobar que la contraseña es la misma
function coincidePass() {
    var pass = $("#password-reg").val();
    var confirmPass = $("#password-confirm-reg").val();
    if (pass != confirmPass) {
        $("#password-confirm-reg").css("background-color","#f8d7da");
        $("#boton-registro").attr("disabled", true);
    } else {
        $("#password-confirm-reg").css("background-color","#d4edda");
        $("#boton-registro").attr("disabled", false);
    }
}

$(document).ready(function(){
    //Registro
    $("#a-registro").click(function(){
        //Cambiamos los botones
        $("#a-login").css('display','block');
        $("#a-registro").css('display','none');
        //Cambiamos los formulario
        $("#form-login").css('display','none');
        $("#form-registro").css('display','block');
    });
    //Login
    $("#a-login").click(function(){
        //Cambiamos los botones
        $("#a-login").css('display','none');
        $("#a-registro").css('display','block');
        //Cambiamos los formulario
        $("#form-login").css('display','block');
        $("#form-registro").css('display','none');
    });

    $("#password-confirm-reg").keyup(coincidePass);
});