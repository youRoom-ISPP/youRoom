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
    $('.crop_image').click(function(event){
        var formData = new FormData();
        image_crop.croppie('result', {type: 'blob', format: 'png'}).then(function(blob) {
            formData.append('cropped_image', blob);
            ajaxFormPost(formData, '/upload-image/');
        });
        $('#uploadimageModal').modal('hide');
    });
});