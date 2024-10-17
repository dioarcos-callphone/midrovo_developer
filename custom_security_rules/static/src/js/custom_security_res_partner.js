odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var core = require('web.core');
    var qweb = core.qweb;

    var FormController = require('web.FormController');

    FormController.include({
        constructor: function (parent, action) {
            this._super(parent, action);
            console.log('FormController extendido'); // Log para verificar que se extiende
        },
        _onButtonNew: function (ev) {
            this._super(ev);
            console.log('¡Se hizo clic en el botón Nuevo!'); // Log al hacer clic en el botón Nuevo
        },
    });

});
