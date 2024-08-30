odoo.define('pos_note_invoice.order_line_note_button', (require) => {
    "use strict";

    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');
    const { useBus } = require('@web/core/utils/hooks');

    const OrderlineCustomerNoteButtonExtend = OrderlineCustomerNoteButton => class extends OrderlineCustomerNoteButton {
        setup() {
            super.setup();
            this.env.posbus = useBus(this.env.posbus, 'order_line_note_updated', this._onOrderLineNoteUpdated.bind(this));
        }

        async onClick() {    
            const { confirmed, payload: inputNote } = await this.showPopup("TextAreaPopup", {
                // startingValue: selectedOrderline.get_customer_note(),
                title: this.env._t("Añadir Nota o Comentario"),
            });
    
            if (confirmed) {
                
                console.log(`Mostrando InputNote >>> ${ inputNote }`)
                this.env.posbus.trigger('order_line_note_updated', { note: inputNote });

            }
        }

        _onOrderLineNoteUpdated(event) {
            console.log(`Nota actualizada: ${event.detail.note}`);
        }

    }

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonExtend);

    return OrderlineCustomerNoteButton;

});
