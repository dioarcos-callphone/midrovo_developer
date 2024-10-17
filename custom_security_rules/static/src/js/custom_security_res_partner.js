odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        _renderButtons: function () {
            this._super.apply(this, arguments);  // Llamar al método original
            var self = this;

            console.log('Renderizando botones de formulario');

            // Verificar permisos del usuario con una llamada RPC
            rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['custom_security_rules.group_custom_security_role_user'],  // Verificar si pertenece al grupo
            }).then(function (hasPermission) {
                if (hasPermission) {
                    // Mostrar los botones de Guardar y Descartar si el usuario tiene permiso
                    self.$buttons.find('.o_form_button_save').show();
                    self.$buttons.find('.o_form_button_cancel').show();
                }
            });
        },
    });
});
