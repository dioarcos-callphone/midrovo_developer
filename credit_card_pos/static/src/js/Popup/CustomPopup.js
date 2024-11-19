odoo.define("credit_card_pos.CustomPopup", (require) => {
    "use strict";

    const { Component } = owl;
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");

    const CustomPopup = (AbstractAwaitablePopup) =>
        class extends AbstractAwaitablePopup {
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

    Registries.Component.extend(AbstractAwaitablePopup, CustomPopup);
});
