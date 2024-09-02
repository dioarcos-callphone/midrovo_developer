odoo.define("pos_note_invoice.order_receipt", function (require) {
    "use strict";

    const { batched, uuidv4 } = require("point_of_sale.utils");

    var { PosGlobalState, Order } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    var rpc = require("web.rpc");
    var Widget = require("web.Widget");

    const PosGlobalStateExtend =  (PosGlobalState) => 
        class PosGlobalStateExtend extends PosGlobalState {
            /* setup() {
                super.setup();
            } */

            async _processData(loadedData) {
                await super._processData(...arguments);
                this.session_orders = loadedData['res.config.settings'];
            } 
            
            async _flush_orders(orders, options) {
                var self = this;
                var result, data;
                let session_orders = self.session_orders;
                var length = session_orders.length-1
                var order_session = session_orders[length]
                
                /* Si el en el config esta activado */
                result = data = super._flush_orders(...arguments);
                //if ( order_session.l10n_ec_sri_payment_ids == true ) {
                    _.each(orders,function(order){
                        data.then(function(){
                            let receipt_number = self.env.pos.selectedOrder.name;
                            let sri_lines = self.env.pos.get_order().export_as_JSON().l10n_ec_sri_payment_ids;

                            if(sri_lines) {
                                rpc.query({ 
                                    model: 'pos.order',
                                    method: 'get_invoice',
                                    args: [receipt_number]
                                    }).then(function(result){
                                        let invocice_name = result.pos_name;
                                        rpc.query({
                                            model: 'account.move',
                                            method: 'update_account_move_sri_lines',
                                            args: [invocice_name, sri_lines]
                                        })
                                    });
                            }
                        });
                    });
                //}
                return result
            }

        }
    
    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
