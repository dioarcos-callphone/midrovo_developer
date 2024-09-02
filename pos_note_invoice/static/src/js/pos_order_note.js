odoo.define('pos_note_invoice.pos_order_note', function (require) {
    "use strict";

    const models = require('point_of_sale.models');

    // Extender el modelo Order
    const _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        // Definir el método set_note_context
        set_note_context: function(note) {
            this.note_context = note;
            this.trigger('change', this); // Dispara un evento de cambio para actualizar la vista si es necesario.
        },

        // Método para obtener el contexto de la nota
        get_note_context: function() {
            return this.note_context || ''; // Retorna la nota almacenada o una cadena vacía si no hay ninguna.
        },

        // Sobrescribir el método export_as_JSON para incluir el contexto de la nota
        export_as_JSON: function() {
            const json = _super_Order.export_as_JSON.apply(this, arguments);
            json.note_context = this.get_note_context();
            return json;
        },
    });
});
