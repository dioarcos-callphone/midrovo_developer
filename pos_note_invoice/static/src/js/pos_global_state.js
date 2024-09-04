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

        async _save_to_server(orders, options) {
            // if (!orders || !orders.length) {
            //     return Promise.resolve([]);
            // }
            // this.set_synch("connecting", orders.length);
            // options = options || {};
    
            // var args = [
            //     _.map(orders, function (order) {
            //         order.to_invoice = options.to_invoice || false;
            //         return order;
            //     }),
            // ];

            // const nota = NoteService.getNote();

            // console.log(`OBTENIENDO NOTA EN POS GLOBAL >>> ${ nota }`)

            // args.push(options.draft || false);

            // console.log(args);

            // rpc.query({
            //     model: 'pos.order',
            //     method: 'create_from_ui',
            //     args: args
            // }).then(function(result) {
            //     console.log(`MOSTRANDO RESULT DE CREATE FROM >>> ${ result }`)
            //     rpc.query({
            //         model: 'pos.order',
            //         method: 'note_update_invoice',
            //         args: [ nota, result ]
            //     }).then(function(result) {
            //         console.log(`MOSTRANDO RESULT DE NOTE UPDATE`)
            //     });

            // });

            const result = await super._save_to_server(orders, options);

            console.log(result)            

            return result
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});
