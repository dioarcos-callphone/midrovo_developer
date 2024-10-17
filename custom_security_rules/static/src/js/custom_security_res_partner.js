odoo.define('custom_security_rules.custom_security_res_partner', function (require) {
    "use strict";

    const KanbanView = require('web.KanbanView');
    const KanbanController = require('web.KanbanController');

    KanbanController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            let $btnNew = this.$el.find('.o-kanban-button-new');
            $btnNew.on('click', this._onNewButtonClick.bind(this));
        },

        _onNewButtonClick: function (event) {
            // Aquí puedes personalizar lo que hace el botón programáticamente
            console.log('Botón nuevo presionado');
        },
    });

});
