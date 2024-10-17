odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    // Importaciones necesarias
    const KanbanController = require('@web/views/kanban/kanban_controller').KanbanController;
    const { patch } = require('@web/core/utils/patch');
    const rpc = require('web.rpc');

    // Parchear el KanbanController para extender su funcionalidad
    patch(KanbanController.prototype, 'custom_security_rules.custom_security_res_partner', {
        async render() {
            await this._super(...arguments);

            console.log('ENTRAAAA')
            
            // Aquí puedes manipular los botones después de que se haya renderizado la vista
            if (this.$buttons) {
                this.checkUserPermissions();
            }
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
                console.log('TIENE PERMISOS')
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
