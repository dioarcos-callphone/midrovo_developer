odoo.define('ec_account_edi_extend.download_with_spinner', function (require) {
    'use strict';

    const core = require('web.core');
    const QWeb = core.qweb;

    $(document).ready(function () {
        // Renderiza el spinner en el DOM
        if (!$('#download-spinner').length) {
            $('body').append(QWeb.render('DownloadSpinner'));
        }

        // Maneja el clic en los enlaces de descarga
        $('.download-link').on('click', function () {
            const spinner = $('#download-spinner');
            spinner.show(); // Muestra el spinner

            // Oculta el spinner después de 5 segundos (o según sea necesario)
            setTimeout(() => {
                spinner.hide();
            }, 5000);
        });
    });
});
