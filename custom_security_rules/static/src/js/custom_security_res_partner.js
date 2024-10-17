odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var core = require('web.core');
    var qweb = core.qweb;

    FormController.include({
        // Método para inicializar el controlador
        _onButtonNew: function (ev) {
            this._super(ev); // Llama al método original para mantener la funcionalidad

            // Agrega un console.log cuando se hace clic en el botón "Nuevo"
            console.log('¡Se hizo clic en el botón Nuevo!');
        },
    });
});
