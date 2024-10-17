/** @odoo-module **/
import { KanbanView } from "@web/views/kanban/kanban_view";

const { patch } = owl;

patch(KanbanView.prototype, "custom_kanban_view", {
    setup() {
        this._super();
    },
    
    createRecord() {
        console.log("Botón Nuevo presionado!");
        // Aquí puedes hacer lo que necesites, como abrir un formulario customizado
        // O heredar más funcionalidades antes o después del comportamiento original
        this._super();
    },
});
