odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    const FormController = require('web.FormController');
    const rpc = require('web.rpc');

    // Extender el FormController
    FormController.include({
        async render() {
            // Llama al método original
            await this._super(...arguments);
            
            // Llama a tu función para verificar permisos
            this.checkUserPermissions();
        },

        async checkUserPermissions() {
            const self = this;

            // Llamar al método RPC para verificar el grupo
            const hasPermission = await rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['custom_security_rules.group_custom_security_role_user'],  // Verificar si pertenece al grupo
            });

            if (hasPermission) {
                // Mostrar los botones de Guardar y Descartar si el usuario tiene permiso
                console.log('ENTRA AQUI TIENE PERMISOS')
                self.$buttons.find('.o_form_button_save').show();
                self.$buttons.find('.o_form_button_cancel').show();
            } else {
                // Ocultar los botones si el usuario no tiene permiso
                self.$buttons.find('.o_form_button_save').hide();
                self.$buttons.find('.o_form_button_cancel').hide();
            }
        },
    });
});
