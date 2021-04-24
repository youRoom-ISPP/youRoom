$(document).on("click", "[id^=btnP]", function () {
    idProducto = this.id.substring(4);
    form = $("#formP"+idProducto);
    botonStripe = form[0][1];
    botonStripe.click();
});