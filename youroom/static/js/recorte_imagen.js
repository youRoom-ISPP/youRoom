$(document).ready(function(){
    var image_crop = $('#formato-imagen').croppie({
        viewport: {
            width: 300,
            height: 300,
            type:'circle' //square
        },
        boundary:{
            width: 300,
            height: 300
        }
    });
    $('#foto-sin-recortar').on('change', function(){
        var reader = new FileReader();
        reader.onload = function (event) {
            image_crop.croppie('bind', {
                url: event.target.result,
            });
        }
        reader.readAsDataURL(this.files[0]);
        $('#modalRecorteFotoPerfil').modal('show');
    });

    $('#recortar-foto').on('click', function(){
        image_crop.croppie('result', {
            size: 'viewport',
            format: 'png',
            type: 'blob'
        }).then(function (blob){
            var fd = new FormData(document.getElementById('form-foto-perfil'));
            fd.append('imagen_recortada', blob);
            $.ajax({
                url: "",
                type: "POST",
                data: fd,
                processData: false,
                contentType: false,
            }).then((response) => {
                if (response["valid"]) {
                    var fotoUrl = URL.createObjectURL(blob);
                    document.getElementById('foto-perfil').src = fotoUrl;
                    $('#modalRecorteFotoPerfil').modal('hide');
                }
            });
        })
     });
});
