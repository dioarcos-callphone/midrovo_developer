odoo.define('pos_note_invoice.order_line_note_button', (require) => {
    "use strict";

    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');
    const { useBus } = require('@web/core/utils/hooks');

    const OrderlineCustomerNoteButtonExtend = OrderlineCustomerNoteButton => class extends OrderlineCustomerNoteButton {
        setup() {
            super.setup();
            // useBus(this.env.bus, 'input-note-event', evento => console.log(evento.detail.note));
        }

        async onClick() {    
            const { confirmed, payload: inputNote } = await this.showPopup("TextAreaPopup", {
                // startingValue: selectedOrderline.get_customer_note(),
                title: this.env._t("Añadir Nota o Comentario"),
            });
    
            if (confirmed) {
                console.log('Disparando evento "input-note-event" con la nota:', inputNote);
                
                // if (this.isEventBus(this.env.bus)) {
                //     console.log('this.env.bus parece ser un EventBus.');
                // } else {
                //     console.log('this.env.bus no es un EventBus.');
                // }

                this.env.bus("input-note-event", { note: inputNote });

            }
        }

        // isEventBus(obj) {
        //     return obj && typeof obj === 'object' && 
        //            typeof obj.on === 'function' &&
        //            typeof obj.off === 'function' &&
        //            typeof obj.trigger === 'function';
        // }

    }

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonExtend);

    return OrderlineCustomerNoteButton;

});
