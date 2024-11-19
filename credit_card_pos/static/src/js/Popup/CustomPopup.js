odoo.define("credit_card_pos.CustomPopup", (require) => {
    "use strict";

    const { Component } = owl;
    const AbstractPopup = require("point_of_sale.AbstractPopup");
    const Registries = require("point_of_sale.Registries");

    const CustomPopup = (AbstractPopup) =>
        class extends AbstractPopup {
            mounted() {
                super.mounted();
                // Emitimos el evento cuando el popup se muestra
                this.trigger("show-popup");
            }

            willUnmount() {
                // Emitimos el evento cuando el popup se cierra
                this.trigger("close-popup");
                super.willUnmount();
            }
        };

    Registries.Component.extend(AbstractPopup, CustomPopup);
});
