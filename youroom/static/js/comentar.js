function enviarComentario(idPublicacion) {
    let comentario = $("#formCom" + idPublicacion)[0][1];
    let csrf = $("#formCom" + idPublicacion)[0][0];
    $.ajax({
        type: "POST",
        url: "/publicacion/comentar/",
        data: {
            form: $("#formCom" + idPublicacion).serialize(),
            texto: comentario.value,
            publicacion_id: idPublicacion,
            csrfmiddlewaretoken: csrf.value
        }
    }).done(function () {
    }).then((response) => {
        location.reload();
    }).fail(function () {
    });
}

$(document).on("click", "[id^=comentarP]", function (e) {
    e.preventDefault();
    let idPublicacion = this.id.substring(9);
    let texto = $("#formCom" + idPublicacion)[0][1];
    if (texto.value.length > 0) {
        enviarComentario(idPublicacion);
    }
});

