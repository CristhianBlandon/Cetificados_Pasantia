document.querySelector('#file').addEventListener('change', function (e) {
  var boxFile = document.querySelector('.boxFile');
  boxFile.classList.remove('attached');
  boxFile.innerHTML = boxFile.getAttribute("data-text");
  if (this.value != '') {
    var allowedExtensions = /(\.pdf)$/i;
    if (allowedExtensions.exec(this.value)) {
      boxFile.innerHTML = e.target.files[0].name;
      boxFile.classList.add('attached');
    }
    else {
      this.value = '';
      alert('El archivo que intentas subir no está permitido.\nLos archivos permitidos son .pdf');
      boxFile.classList.remove('attached');
    }
  }
});

$(document).ready(function() {
  $('#mydatatable tfoot th').each( function () {
      var title = $(this).text();
      $(this).html( '<input type="text" placeholder="Filtrar.." />' );
  } );

  var table = $('#mydatatable').DataTable({
      "dom": 'B<"float-left"i><"float-right"f>t<"float-left"l><"float-right"p><"clearfix">',
      "responsive": false,
      "language": {
          "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
      },
      "order": [[ 0, "desc" ]],
      "initComplete": function () {
          this.api().columns().every( function () {
              var that = this;

              $( 'input', this.footer() ).on( 'keyup change', function () {
                  if ( that.search() !== this.value ) {
                      that
                          .search( this.value )
                          .draw();
                      }
              });
          })
      }
  });
});
