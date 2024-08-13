odoo.define('pos_receipt_add_fields_prueba.PaymentScreen', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
        super.setup();
        }
        async validateOrder(isForceValidate) {
        let receipt_number = this.env.pos.selectedOrder.name;
        var orders = this.env.pos.selectedOrder
        const receipt_order = await super.validateOrder(...arguments);
        var self = this;
        rpc.query({
            model: 'pos.order',
            method: 'get_invoice_field',
            args: [receipt_number]
            }).then(function(result){
                console.log('Ingresa aqui >>>>');
                /* console.log(result) */
                if (result.invoice_name) {
                    console.log(`Mostrando el Cashier Name >>> ${result.cashier_name}`)
                    self.env.pos.user_id = result.cashier_name;
                    /* console.log('data');
                    console.log(result.invoice_name)
                    console.log(result.xml_key) */
                }
            });
            return receipt_order
        }
    }

    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);

    return PaymentScreen;

});