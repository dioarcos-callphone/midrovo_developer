odoo.define("pos_note_invoice.pos_global_state", (require) => {
    "use strict";

    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');
    const NoteService = require('pos_note_invoice.note_service');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {
        // constructor(obj) {
        //     super(obj);
        //     // Puedes agregar o modificar atributos aquí
        // }

        // setup() {
        //     super.setup()
        // }

        _save_to_server(orders, options) {
            if (!orders || !orders.length) {
                return Promise.resolve([]);
            }
            this.set_synch("connecting", orders.length);
            options = options || {};
    
            var args = [
                _.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                }),
            ];

            const nota = NoteService.getNote();

            console.log(`OBTENIENDO NOTA EN POS GLOBAL >>> ${ nota }`)

            args.push(options.draft || false);
            args.push(nota);

            console.log(args);

            rpc.query({
                model: 'pos.order',
                method: 'get_note',
                args: args
            }).then(function(result) {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });
            

            return super._save_to_server(orders, options);
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
