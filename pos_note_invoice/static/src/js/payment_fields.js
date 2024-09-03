odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    const rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const NoteService = require('pos_note_invoice.note_service');

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            this.mostrandoNote();
        }

        mostrandoNote() {
            const nota = NoteService.getNote();
            console.log('NOTA DESDE EL PAYMENT FIELDS >>> ', NoteService.getNote());
            rpc.query({
                model: 'account.move',
                method: 'get_note',
                args: [nota]
            }).then((result) => {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });
        }
    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 