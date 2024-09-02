odoo.define('pos_note_invoice.pos_order_note', function (require) {
    "use strict";

    const models = require('point_of_sale.models');

    const _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        set_note_context: function(note) {
            this.note_context = note;
            this.trigger('change', this);
        },

        get_note_context: function() {
            return this.note_context || '';
        },

        export_as_JSON: function() {
            const json = _super_Order.export_as_JSON.apply(this, arguments);
            json.note_context = this.get_note_context();
            return json;
        },
    });
});
