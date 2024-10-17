odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";
    
    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        _onButtonNew: function (event) {
            // Llamamos al método original para la creación de un nuevo registro
            this._super.apply(this, arguments);

            var self = this;

            // Verificar permisos del usuario con una llamada RPC
            rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['your_module.group_show_save_buttons'],  // Verificar si pertenece al grupo
            }).then(function (hasPermission) {
                if (hasPermission) {
                    // Mostrar los botones de Guardar y Descartar si el usuario tiene permiso
                    self.$buttons.find('.o_form_button_save').show();
                    self.$buttons.find('.o_form_button_cancel').show();
                } else {
                    // Ocultar los botones si el usuario no tiene permiso
                    self.$buttons.find('.o_form_button_save').hide();
                    self.$buttons.find('.o_form_button_cancel').hide();
                }
            });
        },
    });
});