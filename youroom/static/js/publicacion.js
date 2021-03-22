class Etiqueta {
    constructor(nombre, enlace, coordX, coordY) {
        this.nombre = nombre;
        this.enlace = enlace;
        this.coordX = coordX;
        this.coordY = coordY;
    }

    set addEnlace(enlace) {
        this.enlace = enlace;
    }
}

let contadorEtiqueta = 0;
let etiqueta = null;
let listaEtiquetas = [];

function procesarEtiquetas(listaEtiquetas){
    let etiquetasStr = "";
    for(i = 0; i < listaEtiquetas.length; i++){
        let etiqueta = listaEtiquetas[i];
        etiquetasStr += etiqueta.enlace + "," + etiqueta.coordX + "," + etiqueta.coordY + "|"
    }
    return etiquetasStr.substring(0, etiquetasStr.length - 1);
}

function validaEnlace(enlace) {
    let validador = false;
    if(/^(http|https|ftp):\/\/?.*$/i.test(enlace)){
        validador = true;
    }

    return validador;
}

function readURL(input) {
    let validador = true;
    if (input.files && input.files[0]) {
        const tipo = input.files[0].type;
        if (tipo == "image/jpg" || tipo == "image/jpeg" || tipo == "image/png") {
            let reader = new FileReader();
            reader.onload = function (e) {
                $('#visor-imagen').attr('src', e.target.result);
                $('#visor-imagen').show();
            }
            reader.readAsDataURL(input.files[0]);
            validador = true;
        } else {
            validador = false;
        }
    }

    return validador;
}

function getCoords(event, element) {
    const clickLeft = event.clientX;
    const elementLeft = element.offsetLeft;
    let x = (clickLeft - elementLeft) / element.width;
    x = (Math.round(x * 1000) / 1000) - 0.02;

    const clickTop = event.clientY + $(window).scrollTop() + 5;
    const elementTop = element.offsetTop;
    let y = (clickTop - elementTop) / element.height;
    y = (Math.round(y * 1000) / 1000) - 0.02;

    return [x, y];
}

function crearEtiqueta(coords) {
    const x = coords[0] * 100;
    const y = coords[1] * 100;
    const etiquetaID = "#etiqueta" + contadorEtiqueta;
    $("#container-visor").append('<div class="etiqueta" id="etiqueta'
        + contadorEtiqueta + '"><div>');
    $(etiquetaID).css("left", x + '%');
    $(etiquetaID).css("top", y + '%');
    $("#url-etiqueta").removeClass("d-none");
    contadorEtiqueta++;
    return new Etiqueta(etiquetaID, null, x, y);
}

function capturaPulsacion (event) {
    const visor = {
        width: $("#visor-imagen").innerWidth(),
        height: $("#visor-imagen").innerHeight(),
        offsetLeft: $("#visor-imagen").offset().left,
        offsetTop: $("#visor-imagen").offset().top
    };
    $("#instrucciones-subir-foto").hide();
    $('#visor-imagen').off()
    const coords = getCoords(event, visor);
    etiqueta = crearEtiqueta(coords);
}

$("#error-url-enlace").hide();
$("#error-tipo-archivo").hide();
$("#metadata-publicacion").hide();
$('#visor-imagen').toggle();
$("#imagen").change(function (){
    $(".etiqueta").remove();
    $("#enlace-etiqueta").val("");
    $("#url-etiqueta").addClass("d-none");
    $("#error-url-enlace").hide();
    const validaImagen = readURL(this);
    if (validaImagen) {
        $("#error-tipo-archivo").hide();
        $("#icono-subir-foto").removeClass("bi-plus-square");
        $("#icono-subir-foto").addClass("bi-arrow-clockwise");
        $("#metadata-publicacion").show();
        $("#instrucciones-subir-foto").text("Etiqueta los productos y elige una categoría para tu publicación");
        $(".etiqueta").remove();
        contadorEtiqueta = 0;
        etiqueta = null;
        listaEtiquetas = [];
    } else {
        $("#error-tipo-archivo").show();
    }
});

$('#visor-imagen').on('click', capturaPulsacion);

$("#btn-borrar-enlace").click(function () {
    if ($("#error-url-enlace").is(":visible")) {
        console.log("entra")
        $("#error-url-enlace").hide();
        $(".etiqueta").last().remove();
    }
    $("#enlace-etiqueta").val("");
    $("#etiqueta" + (contadorEtiqueta - 1)).remove();
    etiqueta = null;
    $("#url-etiqueta").addClass("d-none");
    $("#instrucciones-subir-foto").show();
    return $('#visor-imagen').on('click', capturaPulsacion);
});

$("#btn-guardar-enlace").click(function () {
    $("#error-url-enlace").hide();
    const enlace = $("#enlace-etiqueta").val();
    if (validaEnlace(enlace)) {
        etiqueta.addEnlace = enlace;
        $("#enlace-etiqueta").val("");
        $("#instrucciones-subir-foto").show();
        $("#url-etiqueta").addClass("d-none");
        listaEtiquetas.push(etiqueta);
        return $('#visor-imagen').on('click', capturaPulsacion);
    } else {
        $("#error-url-enlace").show();
    }
});

$("#btnPublicar").click(function () {
    const etiquetasStr = procesarEtiquetas(listaEtiquetas);
    $("#etiquetas").val(etiquetasStr);
});
