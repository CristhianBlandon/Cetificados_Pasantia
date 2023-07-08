$(document).ready(function () {

    table = $('table.display').DataTable({


        "language": {

            url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'

        },

        responsive: true,

        dom: "<'row'<'col-sm-12 col-md-6 pt-2'B><'col-sm-12 col-md-6'f>><'row'<'col-sm-12 col-md-6 pt-2'>>" +
        "<'row'<'col-sm-12 overflow-auto'rt>>" +
        "<'row'<'col-sm-12 col-md-6'i><'col-sm-12 col-md-6'p>>" + "<'row'<'col-sm-12 col-md-6'l>>",

        buttons: [
            {
				extend:    'excelHtml5',
				text:      '<i class="fas fa-file-excel"></i> ',
				titleAttr: 'Exportar a Excel',
				className: 'btn btn-success'
			},
			{
				extend:    'pdfHtml5',
				text:      '<i class="fas fa-file-pdf"></i> ',
				titleAttr: 'Exportar a PDF',
				className: 'btn btn-danger'
			},
			{
				extend:    'print',
				text:      '<i class="fa fa-print"></i> ',
				titleAttr: 'Imprimir',
				className: 'btn btn-info'
			},
        ],

        

    });

});