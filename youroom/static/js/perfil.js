$(document).ready(function(){
    $("#vida-semanal").click(function(){
        $("[data-toggle='vida-semanal']").popover('show');
    });
});
$(document).ready(function(){
    $("#vida-comprada").click(function(){
        $("[data-toggle='vida-comprada']").popover('show');
    });
});
$(document).ready(function(){
    $("#publicaciones-totales").click(function(){
        $("[data-toggle='publicaciones-totales']").popover('show');
    });
});
$(document).ready(function(){
    $("#puntos-totales").click(function(){
        $("[data-toggle='puntos-totales']").popover('show');
    });
});

$("#btnCancelarSus").click(function () {
    $("#btnCancelarSus").html("<span id=\"spinnerBtn\"></span> Cancelando suscripción...")
    $("#spinnerBtn").addClass("spinner-border");
    $("#spinnerBtn").addClass("spinner-border-sm");
    $("#spinnerBtn").attr("role", "status");
    $("#spinnerBtn").attr("aria-hidden", "true");
});

$("#btnSus").click(function () {
    $("#btnSus").html("<span id=\"spinnerBtn\"></span> Abriendo formulario...")
    $("#spinnerBtn").addClass("spinner-border");
    $("#spinnerBtn").addClass("spinner-border-sm");
    $("#spinnerBtn").attr("role", "status");
    $("#spinnerBtn").attr("aria-hidden", "true");
});