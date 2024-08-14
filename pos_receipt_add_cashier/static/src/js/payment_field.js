odoo.define('pos_receipt_add_cashier.PaymentScreen', function (require) {
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
                  if (result.invoice_name) {
                     self.env.pos.cashier  = result.cashier_name
                  }
               });
               return receipt_order
         }
      }

      Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);

      return PaymentScreen;
   });
