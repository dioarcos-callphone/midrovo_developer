odoo.define('pos_note_invoice.payment_fields', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { useBus, useService } = require('@web/core/utils/hooks');
    const { EventBus } = require("@odoo/owl");

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
            super.setup();
            // this.actionService = useService("action");
            // this.ui = useService('ui');
            this.inputNote = ''
            const bus = this.env.bus || new EventBus();
            useBus(bus, 'input-note-event', event => this.noteUpdate(event));

        }

        noteUpdate(evento) {
            console.log(evento.detail.note);
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
 