odoo.define('pos_note_invoice.order_line_note_button', (require) => {
    "use strict";

    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('@web/core/utils/hooks');


    const OrderlineCustomerNoteButtonExtend = OrderlineCustomerNoteButton => class extends OrderlineCustomerNoteButton {
        setup() {
            super.setup();
            this.note = ''
            useListener('note-update', this.noteInput)
            this.getNote()
        }

        getNote() {
            console.log(`MOSTRANDO EVENTO >>> ${ this.note }`)
        }

        async onClick() {    
            const { confirmed, payload: inputNote } = await this.showPopup("TextAreaPopup", {
                // startingValue: selectedOrderline.get_customer_note(),
                title: this.env._t("Añadir Nota o Comentario"),
            });
    
            if (confirmed) {
                console.log('Esta es la nota:', inputNote);
                // this.env.pos.get_order().set_note_context(inputNote);
                this.trigger('note-update', { note: inputNote });
                // this.env.note_context = inputNote;

            }
        }

        noteInput(event) {
            this.note = event.detail.note
            console.log(`MOSTRANDO EVENTO >>> ${ event.detail.note }`)
        }

    }

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonExtend);

    return OrderlineCustomerNoteButton;

});
