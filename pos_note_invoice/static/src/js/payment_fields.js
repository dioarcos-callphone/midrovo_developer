odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    const rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const NoteService = require('pos_note_invoice.note_service');

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            // this.mostrandoNote();
        }

        async _postPushOrderResolve(order, order_server_ids) {
            const receipt_number = this.env.pos.selectedOrder.name;
            const argumentos = {
                'receipt_number': receipt_number,
                'note': NoteService.getNote()
            }

            const nota = NoteService.getNote()

            rpc.query({
                model: 'account.move',
                method: 'get_note',
                args: [ argumentos ]
            }).then(function(result) {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });

            return true;
        }

    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 