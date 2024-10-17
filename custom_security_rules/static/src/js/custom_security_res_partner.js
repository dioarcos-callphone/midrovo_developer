import { KanbanController } from "@web/views/kanban/kanban_controller";  // Si es necesario manipular el controlador
import { registry } from "@web/core/registry";  // Para manejar registros si lo necesitas

const KanbanControllerExtended = KanbanController.extend({
    createRecord: function () {
        console.log("Botón Nuevo presionado!");
        this._super();
    }
});

registry.category("views").add("kanban", KanbanControllerExtended);
