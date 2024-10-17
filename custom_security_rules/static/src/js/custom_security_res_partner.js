odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    // Importaciones necesarias
    const KanbanController = require('@web/views/kanban/kanban_controller').KanbanController;
    const { patch } = require('@web/core/utils/patch');
    const rpc = require('web.rpc');

    // Parchear el KanbanController para extender su funcionalidad
    patch(KanbanController.prototype, 'custom_security_rules.custom_security_res_partner', {
        createRecord() {
            const self = this;

            // Llamar al método RPC para verificar el grupo
            rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['custom_security_rules.group_custom_security_role_user'],  // Verificar si pertenece al grupo
            }).then(function (hasPermission) {
                if (hasPermission) {
                    // Mostrar los botones de Guardar y Descartar si el usuario tiene permiso
                    console.log('ENTRA TIENE PERMISOS')
                    
                    document.querySelectorAll('.o_form_button_save').forEach(button => {
                        button.style.display = 'none';  // Oculta el botón
                    });
                    
                    document.querySelectorAll('.o_form_button_cancel').forEach(button => {
                        button.style.display = 'none';  // Oculta el botón
                    });
                }
            });

            // Llama al método original de createRecord
            return this._super(...arguments);
        },
    });
});
