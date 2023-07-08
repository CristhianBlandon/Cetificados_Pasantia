$(function() {
    $("#nombre_razonsocial").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin/certificados/Search_Nombre",
                data: {
                    term : request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2
    });
    $("#nombre_razonsocial").on("blur", function() {
        var valor = $(this).val();
        if (valor) {
            $.ajax({
                url: "/admin/certificados/Mostar_Nombre",
                data: {
                    valor: valor
                },
                success: function(data) {
                    var tipo_docInput = $("#tipo_doc_proveedor");
                    tipo_docInput.val(data[0][0]);
                    var num_provInput = $("#num_iden_proveedor");
                    num_provInput.val(data[0][1]);
                    var emailInput = $("#email");
                    emailInput.val(data[0][2]);
                }
            });
        }
    });
});