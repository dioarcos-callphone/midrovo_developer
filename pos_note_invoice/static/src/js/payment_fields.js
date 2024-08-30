odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;
    const { useBus, useService } = require('web.core.utils.hooks');
    // const { useBus } = require('web.core.utils.hooks'); 
 
    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            this.ui = useService('ui');
            useBus(this.ui.bus, 'order_line_note_updated', event => {
                console.log(event)
            });
            // this.bus = useBus(this.env.bus, 'order_line_note_updated', this._onOrderLineNoteUpdated.bind(this));
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

        // _onOrderLineNoteUpdated(event) {
        //     // Maneja la nota recibida
        //     const note = event.detail.note;
        //     console.log(`Nota recibida en PaymentScreen: ${note}`);
        //     // Aquí puedes hacer algo con la nota, como actualizar el estado del pedido
        // }
    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 