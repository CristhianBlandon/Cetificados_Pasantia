//---------------------------------------------------------------------------------------//
//                          Script de Envio De Certificado                              //
//-------------------------------------------------------------------------------------//
function envioEmail() {
  document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    const deleteUrl = event.target.action;
    Swal.fire({
      title: '¿Has verificado que los datos ingresados sean correctos?',
      text: "verifica que todos los datos ingresados sean correctos, y de a ver completado cada campo de solicitud",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#0D6EFD',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Solicitar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true,
      showClass: {
        popup: 'animate__animated animate__fadeInDown'
      },
      hideClass: {
        popup: 'animate__animated animate__fadeOutUp'
      },
      customClass: {
        confirmButton: 'btn btn-primary float-right',
        cancelButton: 'btn btn-secondary'
      }
    })
      .then((result) => {
        if (result.isConfirmed) {
          const spinner = Swal.fire({
            title: 'Espere porfavor...',
            html: 'No cierre la ventana del navegador',
            timerProgressBar: true,
            didOpen: () => {
              Swal.showLoading()
            },
          });
          fetch(deleteUrl, {
            method: 'POST',
            body: new FormData(event.target)
          })
            .then(response => response.json())
            .then(data => {
              if (data.estado === "Enviado") { 
                Swal.fire(
                  data.estado,
                  data.msg,
                  'success'
                ).then(() => {
                  // Redireccionar a la página de lista de elementos
                  window.location.href = data.url;
                });
              } else {
                Swal.fire(
                  data.estado,
                  data.msg,
                  'error'
                ).then(() => {
                  // Redireccionar a la página de lista de elementos
                  window.location.href = data.url;
                });
              }
            })
            .catch(error => {
              Swal.fire(
                data.estado,
                data.msg,
                'error'
              ).then(() => {
                // Redireccionar a la página de lista de elementos
                window.location.href = data.url;
              });
            });
        }
      });
  });
}

//---------------------------------------------------------------------------------------//
//                            Script de Guardar registro                                //
//-------------------------------------------------------------------------------------//
function saveConfirmation() {
  document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    const deleteUrl = event.target.action;
    Swal.fire({
      title: '¿Quieres guardar el registro?',
      text: "Se guardará en la base de datos",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#008000',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, guardar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true,
      showClass: {
        popup: 'animate__animated animate__fadeInDown'
      },
      hideClass: {
        popup: 'animate__animated animate__fadeOutUp'
      },
      customClass: {
        confirmButton: 'btn btn-primary float-right',
        cancelButton: 'btn btn-secondary'
      }
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(deleteUrl, {
          method: 'POST',
          body: new FormData(event.target)
        })
          .then(response => response.json())
          .then(data => {
            if (data.estado === "Correcto") {
              Swal.fire(
                data.estado,
                data.msg,
                'success'
              ).then(() => {
                // Redireccionar a la página de lista de elementos
                window.location.href = data.url;
              });
            } else {
              Swal.fire(
                data.estado,
                data.msg,
                'error'
              ).then(() => {
                // Redireccionar a la página de lista de elementos
                window.location.href = data.url;
              });
            }
          })
          .catch(error => {
            Swal.fire(
              'Error',
              'Los datos insertados no fueron posible guardarlos.',
              'error'
            );
          });
      }
    });
  });
}

//---------------------------------------------------------------------------------------//
//                             Script de Editar registro                                //
//-------------------------------------------------------------------------------------//
function editConfirmation() {
  document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    const deleteUrl = event.target.action;
    Swal.fire({
      title: '¿Quieres actualizar el registro?',
      text: "Se actualizara en la base de datos",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#008000',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, Actualizar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true,
      showClass: {
        popup: 'animate__animated animate__fadeInDown'
      },
      hideClass: {
        popup: 'animate__animated animate__fadeOutUp'
      },
      customClass: {
        confirmButton: 'btn btn-primary float-right',
        cancelButton: 'btn btn-secondary'
      }
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(deleteUrl, {
          method: 'POST',
          body: new FormData(event.target)
        })
          .then(response => response.json())
          .then(data => {
            if (data.estado === "Correcto") {
              Swal.fire(
                data.estado,
                data.msg,
                'success'
              ).then(() => {
                // Redireccionar a la página de lista de elementos
                window.location.href = data.url;
              });
            } else {
              Swal.fire(
                data.estado,
                data.msg,
                'error'
              ).then(() => {
                // Redireccionar a la página de lista de elementos
                window.location.href = data.url;
              });
            }
          })
          .catch(error => {
            Swal.fire(
              'Error',
              'Ha ocurrido un error al actualizar el registro.',
              'error'
            );
          });
      }
    });
  });
}

//---------------------------------------------------------------------------------------//
//                            Script de Eliminar registro                               //
//-------------------------------------------------------------------------------------//
function deleteConfirmation(button) {
  const deleteUrl = button.dataset.deleteUrl;
  Swal.fire({
    title: '¿Está seguro?',
    text: "No podrás revertir esto.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#008000',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
    reverseButtons: true,
    showClass: {
      popup: 'animate__animated animate__fadeInDown'
    },
    hideClass: {
      popup: 'animate__animated animate__fadeOutUp'
    },
    customClass: {
      confirmButton: 'btn btn-primary float-right',
      cancelButton: 'btn btn-secondary'
    }
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(deleteUrl, {
        method: 'GET'
      })
        .then(response => response.json())
        .then(data => {
          if (data.estado === "Correcto") {
            Swal.fire(
              data.estado,
              data.msg,
              'success'
            ).then(() => {
              // Redireccionar a la página de lista de elementos
              window.location.href = data.url;
            });
          } else {
            Swal.fire(
              data.estado,
              data.msg,
              'error'
            ).then(() => {
              // Redireccionar a la página de lista de elementos
              window.location.href = data.url;
            });
          }
        })
        .catch(error => {
          Swal.fire(
            'Error',
            'Ha ocurrido un error al eliminar los datos.',
            'error'
          );
        });
    }
  });
}