odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;
    const { eventBus } = require('web.core');

 
    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            this.eventBus = eventBus;
            this.eventBus.on('order-line-note-updated', this, this._onOrderLineNoteUpdated);
          }

        _onOrderLineNoteUpdated(eventData) {
            const { note } = eventData.detail;
            console.log(`Nota recibida en PaymentScreen: ${note}`);
            // Aquí puedes usar inputNote como desees
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
                   console.log('data field 1');
                   /* console.log(result) */
                   if (result.invoice_name) {
                      self.env.pos.invoice  = result.invoice_name
                      self.env.pos.invoice_xml_key  = result.xml_key
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
 