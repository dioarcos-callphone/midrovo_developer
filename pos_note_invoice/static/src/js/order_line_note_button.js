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
                startingValue: NoteService.getNote(),
                title: this.env._t("Añadir Nota o Comentario"),
            });
    
            if (confirmed) {
                const longitud = inputNote.length

                if(longitud > 200) {
                    const { confirmed: continueConfirmation } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Advertencia'),
                        body: this.env._t('El comentario excede los 200 caracteres. ¿Deseas continuar?'),
                    });

                    if (!continueConfirmation) {
                        return;
                    }
                    
                }

                console.log(longitud)
                NoteService.setNote(inputNote);
            }
        }
    }

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonExtend);

    return OrderlineCustomerNoteButton;

});
