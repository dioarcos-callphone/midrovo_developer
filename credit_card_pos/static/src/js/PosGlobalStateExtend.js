odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {

            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);
            console.log(this.payment_methods)
            //console.log(result)

            await rpc.query({
                model: 'pos.order',
                method: 'update_invoice_payments_widget',
                args: [ result ]
            })

            return result
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
