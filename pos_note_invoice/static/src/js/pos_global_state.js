odoo.define("pos_note_invoice.pos_global_state", (require) => {
    "use strict";

    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
    const NoteService = require('pos_note_invoice.note_service');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {

            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);

            const nota = NoteService.getNote();

            await rpc.query({
                model: 'pos.order',
                method: 'note_update_invoice',
                args: [ nota, result ]
            })

            NoteService.setNote('');

            return result
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
