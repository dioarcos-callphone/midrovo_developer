odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var core = require('web.core');

    FormController.include({
        _onButtonNew: function (ev) {
            console.log('¡Se hizo clic en el botón Nuevo!');
            this._super(ev); // Asegúrate de que esto se llame después de tu código
        },
    });
});
