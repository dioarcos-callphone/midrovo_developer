odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { useBus } = require("web.core.utils.hooks");
    

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            // this.bus = useBus();  // Configura el bus
            // this.bus.on('inputNote:updated', event => {
            //     console.log(event)
            // });
            useBus(this.env.bus, "note", event => {
                console.log(event);
            });
                
        }

        // _onInputNoteUpdated({ inputNote }) {
        //     console.log(`Recibido InputNote en PaymentScreen >>> ${inputNote}`);
        //     this.inputNote = inputNote; // Ejemplo de uso
        // }

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
                   console.log('*** ENTRA AQUI ***');
                   if (result.invoice_name) {
                      self.env.pos.invoice  = result.invoice_name
                      self.env.pos.invoice_xml_key  = result.xml_key        
                   }
                });
                return receipt_order
        }
    }
 
    Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);
 
    return PaymentScreen;
});
 