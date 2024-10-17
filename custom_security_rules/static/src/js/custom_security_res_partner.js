odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    // Importaciones necesarias
    const KanbanController = require('@web/views/kanban/kanban_controller').KanbanController;
    const { patch } = require('@web/core/utils/patch');
    const rpc = require('web.rpc');

    // Parchear el KanbanController para extender su funcionalidad
    patch(KanbanController.prototype, 'custom_security_rules.custom_security_res_partner', {
        createRecord() {
            // Realiza la consulta RPC para verificar el grupo
            rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['custom_security_rules.group_custom_security_role_user'],  // Verificar si pertenece al grupo
            }).then((hasPermission) => {  // Función flecha aquí
                console.log(this);  // Verifica el valor de `this`, que debe ser la instancia de KanbanController
                if (hasPermission) {
                    console.log('ENTRA TIENE PERMISOS');
                    // Usa this.$buttons para acceder a la propiedad de la instancia
                    if (this.$buttons) {
                        this.$buttons.find('.o_form_button_save').show();
                        this.$buttons.find('.o_form_button_cancel').show();
                    } else {
                        console.error('this.$buttons is undefined');
                    }
                }
            });

            // Llama al método original de createRecord
            return this._super(...arguments);
        },
    });
});
