odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();

        }

        async validateOrder(isForceValidate) {
            let receipt_number = this.env.pos.selectedOrder.name;
            const orders = this.env.pos.selectedOrder
            const receipt_order = await super.validateOrder(...arguments);
            var self = this;

            console.log(orders.orderlines)

            rpc.query({
                model: 'account.move',
                method: 'note_update',
                args: ['NOTA ACTUALIZADA']
                }).then(function(result){
                   console.log(`*** NOTA ACTUALIZADA ***  ${ result }`);
                });
                return receipt_order
        }
    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 