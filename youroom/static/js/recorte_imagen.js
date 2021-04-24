$(document).ready(function(){
    var image_crop = $('#image_demo').croppie({
        viewport: {
            width: 400,
            height: 400,
            type:'circle' //square
        },
        boundary:{
            width: 600,
            height: 400
        }
    });
    $('#cover_image').on('change', function(){
        var reader = new FileReader();
        reader.onload = function (event) {
            image_crop.croppie('bind', {
                url: event.target.result,
            });
        }
        reader.readAsDataURL(this.files[0]);
        $('#uploadimageModal').modal('show');
    });

    $('.crop_image').on('click mousedown touchstart', function(event){
        image_crop.croppie('result', {
            size: 'viewport',
            format: 'png',
            type: 'blob'
        }).then(function (blob){
            var fd = new FormData(document.getElementById('foto-perfil'));
            fd.append('imagen_recortada', blob);
            $.ajax({
            url: "",
            type: "POST",
            data: fd,
            processData: false,
            contentType: false,
            });
            $('#uploadImageModal').modal('hide');
        })
     });
});
