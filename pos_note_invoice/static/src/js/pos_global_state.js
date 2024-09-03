odoo.define('pos_note_invoice.pos_global_state', (require) => {
    const { PosGlobalState } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    const rpc = require("web.rpc");
    const NoteService = require('pos_note_invoice.note_service');

    const PosGlobalStateExtend = PosGlobalState => class extends PosGlobalState {
        setup() {
            super.setup();
            this.obteniendoNotaCashier()
        }

        obteniendoNotaCashier() {
            const nota = NoteService.getNote();
            console.log(`OBTENIENDO NOTA DEL ORDER LINE NOTE >>> ${ nota }`)
            rpc.query({
                model: 'account.move',
                method: 'get_note',
                args: [nota]
            }).then(function(result) {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });
        }

        mostrandoNote() {
            console.log('NOTA DESDE EL PAYMENT FIELDS >>> ', NoteService.getNote());
        }

    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});