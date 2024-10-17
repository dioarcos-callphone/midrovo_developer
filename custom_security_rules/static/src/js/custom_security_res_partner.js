odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    // Importaciones necesarias
    const KanbanController = require('@web/views/kanban/kanban_controller').KanbanController;
    const { patch } = require('@web/core/utils/patch');

    // Parchear el KanbanController para extender su funcionalidad
    patch(KanbanController.prototype, 'custom_security_rules.custom_security_res_partner', {
        createRecord() {
            console.log("Botón Nuevo presionado!");
            return this._super(...arguments);  // Llama al método original
        },
    });

});
