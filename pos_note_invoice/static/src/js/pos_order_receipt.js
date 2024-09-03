odoo.define("pos_note_invoice.pos_order_receipt", function (require) {
    "use strict";

    var { PosGlobalState, Order } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    var rpc = require("web.rpc");
    const NoteService = require('pos_note_invoice.note_service');

    const PosGlobalStateExtend =  (PosGlobalState) => 
        class PosGlobalStateExtend extends PosGlobalState {
            setup() {
                super.setup();
            }

            async _processData(loadedData) {
                await super._processData(...arguments);
                this.session_orders = loadedData['res.config.settings'];
            } 
            
            async _flush_orders(orders, options) {
                const nota = NoteService.getNote();

                rpc.query({
                    model: 'account.move',
                    method: 'get_note',
                    args: [ nota ]
                }).then(function(result) {
                    console.log(`MOSTRANDO RESULT >>> ${ result }`)
                });

            }

        }
    
    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});