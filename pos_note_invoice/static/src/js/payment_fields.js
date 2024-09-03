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

        async validateOrder(isForceValidate) {
            const nota = NoteService.getNote();
            console.log('NOTA DESDE EL PAYMENT FIELDS >>> ', NoteService.getNote());
            rpc.query({
                model: 'account.move',
                method: 'get_note',
                args: [ nota ]
            }).then(function(result) {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });

            let receipt_number = this.env.pos.selectedOrder.name;
            var orders = this.env.pos.selectedOrder
            const receipt_order = await super.validateOrder(...arguments);
            var self = this;

            rpc.query({
               model: 'pos.order',
               method: 'get_invoice_field',
               args: [receipt_number]
            }).then(function(result){
                if (result.invoice_name) {
                    self.env.pos.invoice  = result.invoice_name
                    self.env.pos.invoice_xml_key  = result.xml_key
                }
               });
               return receipt_order
         }

        // mostrandoNote() {
        //     const nota = NoteService.getNote();
        //     console.log('NOTA DESDE EL PAYMENT FIELDS >>> ', NoteService.getNote());
        //     rpc.query({
        //         model: 'account.move',
        //         method: 'get_note',
        //         args: [ nota ]
        //     }).then(function(result) {
        //         console.log(`MOSTRANDO RESULT >>> ${ result }`)
        //     });
        // }
    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 