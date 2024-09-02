odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { useBus, useService } = require('@web/core/utils/hooks');

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            this.ui = useService('ui');
            this.inputNote = ''

        }

        // onInputNoteEvent(event) {
        //     this.inputNote = event.note
        //     console.log('Nota recibida:', event.note);
        //     // Aquí puedes manejar la nota recibida, por ejemplo, asignarla a un campo o mostrarla en la interfaz.
        // }

        async validateOrder(isForceValidate) {
            let receipt_number = this.env.pos.selectedOrder.name;
            var orders = this.env.pos.selectedOrder
            const receipt_order = await super.validateOrder(...arguments);
            var self = this;

            useBus(this.ui.bus, 'input-note-event', event => {
                // this.onInputNoteEvent(event);
                console.log(`OBTENIENDO LA NOTA DEL VENDEDOR >>> ${ event.note }`)
            });

            console.log('Nota almacenada:', this.inputNote);

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
 