function enviarValoracion(valoracion) {
    let idPublicacion = valoracion.id.substring(6);
    let csrf = $("#v" + idPublicacion)[0][0];
    $.ajax({
        type: "POST",
        url: "/timeline/valorar/",
        data: {
            form: $("#v" + idPublicacion).serialize(),
            puntuacion: valoracion.value,
            publicacion_id: idPublicacion,
            csrfmiddlewaretoken: csrf.value
        }
    }).done(function () {
    }).then((response) => {
        if (response["valid"]) {
            $("#" + valoracion.id).prop("checked", true);
        }
    }).fail(function () {
    });
}

$(document).on("click", "[id^=star1P]", function (e) {
    e.preventDefault();
    enviarValoracion(this);
});

$(document).on("click", "[id^=star2P]", function (e) {
    e.preventDefault();
    enviarValoracion(this);
});

$(document).on("click", "[id^=star3P]", function (e) {
    e.preventDefault();
    enviarValoracion(this);
});

$(document).on("click", "[id^=star4P]", function (e) {
    e.preventDefault();
    enviarValoracion(this);
});

$(document).on("click", "[id^=star5P]", function (e) {
    e.preventDefault();
    enviarValoracion(this);
});
