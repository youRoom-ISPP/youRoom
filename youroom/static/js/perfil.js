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

$(document).ready(function () {
    consultarFechaCancelacion();
});

$("#btnCancelarSus").click(function () {
    $("#btnCancelarSus").html("<span id=\"spinnerBtn\"></span> Cancelando suscripción...")
    $("#spinnerBtn").addClass("spinner-border");
    $("#spinnerBtn").addClass("spinner-border-sm");
    $("#spinnerBtn").attr("role", "status");
    $("#spinnerBtn").attr("aria-hidden", "true");
});

$("#btnSus").click(function () {
    $(".stripe-button-el").click();
    $("#btnSus").html("<span id=\"spinnerBtn\"></span> Procesando...")
    $("#spinnerBtn").addClass("spinner-border");
    $("#spinnerBtn").addClass("spinner-border-sm");
    $("#spinnerBtn").attr("role", "status");
    $("#spinnerBtn").attr("aria-hidden", "true");
});

function consultarFechaCancelacion() {
    $.ajax({
        type: 'GET',
        url: '/tienda/obtener_fecha_cancelacion/',
    }).done(function () {
        console.log("Enviada fecha de la próxima facturación del pago");
    }).then(response => {
        if (response['valid']) {
            let d = new Date(response['fechaCancelacion']);
            let ye = new Intl.DateTimeFormat('es', { year: 'numeric' }).format(d);
            let mo = new Intl.DateTimeFormat('es', { month: '2-digit' }).format(d);
            let da = new Intl.DateTimeFormat('es', { day: '2-digit' }).format(d);
            $('#fechaCancelacion').text(` (${da}-${mo}-${ye}).`);
        } else {
            $('#cancelSusModal').addClass('disabled')
        }
    }).fail(function () {
        console.log("Error");
    });
}