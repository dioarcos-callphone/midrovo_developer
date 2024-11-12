odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {
            const creditCards = this.env.pos.creditCards || [];

            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);

            if(creditCards) {
                await rpc.query({
                    model: 'account.move',
                    method: 'update_invoice_payments_widget',
                    args: [ creditCards, result ]
                })

                // Limpiamos la lista de tarjetas de crédito después de enviarlas
                this.env.pos.creditCards = [];

            }

            return result
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
