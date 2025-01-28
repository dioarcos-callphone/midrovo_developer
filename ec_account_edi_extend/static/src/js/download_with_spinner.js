odoo.define('ec_account_edi_extend.download_with_spinner', function (require) {
    'use strict';

    var $ = require('jquery');

    $(document).ready(function () {
        // Evento cuando se hace clic en los íconos de descarga
        $('.download-link').on('click', function (e) {
            // Mostrar el spinner de carga
            $('#spinner-container').show();
            
            // Guardar el href del enlace para que la descarga se inicie después de mostrar el spinner
            var downloadLink = $(this).attr('href');

            // Temporizador para ocultar el spinner después de un tiempo estimado (ajustable)
            setTimeout(function () {
                // Redirigir a la URL de descarga y ocultar el spinner
                window.location.href = downloadLink;
                $('#spinner-container').hide();
            }, 500); // Ajusta el tiempo según sea necesario
        });
    });
});
