odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {

            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);

            const creditCard = this.payment_methods
            .filter(tarjeta => tarjeta.credit_card)  // Filtra objetos que tienen 'credit_card'
            .map(tarjeta => tarjeta.credit_card);    // Mapea solo el diccionario 'credit_card'

            // Eliminamos la propiedad credit_card de los objetos que la contienen
            this.payment_methods.forEach(tarjeta => {
                if (tarjeta.credit_card) {
                    delete tarjeta.credit_card;  // Elimina la propiedad credit_card
                }
            });

            if(creditCard) {
                await rpc.query({
                    model: 'pos.order',
                    method: 'update_invoice_payments_widget',
                    args: [ creditCard, result ]
                })
            }

            return result
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});