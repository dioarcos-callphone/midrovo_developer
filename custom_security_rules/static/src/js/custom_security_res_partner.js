odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    // Importaciones necesarias
    const KanbanController = require('@web/views/kanban/kanban_controller').KanbanController;
    const { patch } = require('@web/core/utils/patch');
    const rpc = require('web.rpc');

    // Parchear el KanbanController para extender su funcionalidad
    patch(KanbanController.prototype, 'custom_security_rules.custom_security_res_partner', {
        createRecord() {
            // No es necesario usar self, ya que utilizamos una función flecha
            rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['custom_security_rules.group_custom_security_role_user'],  // Verificar si pertenece al grupo
            }).then((hasPermission) => {  // Función flecha aquí
                console.log(this);  // Ahora `this` se refiere a la instancia de KanbanController
                if (hasPermission) {
                    console.log('ENTRA TIENE PERMISOS');
                    this.$buttons.find('.o_form_button_save').show();
                    this.$buttons.find('.o_form_button_cancel').show();
                }
            });

            // Llama al método original de createRecord
            return this._super(...arguments);
        },
    });
});
