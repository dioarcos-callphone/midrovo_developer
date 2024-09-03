odoo.define('pos_note_invoice.order_line_note_button', (require) => {
    "use strict";

    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');
    const NoteService = require('pos_note_invoice.note_service');


    const OrderlineCustomerNoteButtonExtend = OrderlineCustomerNoteButton => class extends OrderlineCustomerNoteButton {
        setup() {
            super.setup();
        }

        async onClick() {    
            const { confirmed, payload: inputNote } = await this.showPopup("TextAreaPopup", {
                // startingValue: selectedOrderline.get_customer_note(),
                title: this.env._t("Añadir Nota o Comentario"),
            });
    
            if (confirmed) {
                console.log('Esta es la nota:', inputNote);
                NoteService.setNote(inputNote);
                console.log(NoteService.getNote());
            }
        }

        noteInput(event) {
            console.log(`MOSTRANDO EVENTO >>> ${ event.detail.note }`)
        }

    }

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonExtend);

    return OrderlineCustomerNoteButton;

});
