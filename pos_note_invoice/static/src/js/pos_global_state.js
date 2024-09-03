odoo.define('invoice_update_fields.pos_global_state', (require) => {
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
                args: [note]
            }).then((result) => {
                console.log(`MOSTRANDO RESULT >>> ${ result }`)
            });
        }

        mostrandoNote() {
            console.log('NOTA DESDE EL PAYMENT FIELDS >>> ', NoteService.getNote());
        }

    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);

});