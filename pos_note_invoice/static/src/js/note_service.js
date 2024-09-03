odoo.define('pos_note_invoice.note_service', function (require) {
    "use strict";

    class NoteService {
        constructor() {
            this.note = null;
        }

        setNote(note) {
            this.note = note;
        }

        getNote() {
            return this.note;
        }
    }

    return new NoteService();
});
