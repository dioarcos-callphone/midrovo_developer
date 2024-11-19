odoo.define("credit_card_pos.CustomPopup", (require) => {
    "use strict";

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");

    const CustomPopup = (AbstractAwaitablePopup) =>
        class extends AbstractAwaitablePopup {
            mounted() {
                super.mounted();
                // Emitimos el evento cuando el popup se muestra
                this.env.posbus.trigger("show-popup", { popupId: this.props.id });
            }

            willUnmount() {
                // Emitimos el evento cuando el popup se cierra
                this.env.posbus.trigger("close-popup", { popupId: this.props.id });
                super.willUnmount();
            }

            async confirm() {
                // Sobrescribimos confirm para emitir evento adicional
                await super.confirm();
                this.env.posbus.trigger("close-popup", {
                    popupId: this.props.id,
                    response: { confirmed: true },
                });
            }

            cancel() {
                // Sobrescribimos cancel para emitir evento adicional
                super.cancel();
                this.env.posbus.trigger("close-popup", {
                    popupId: this.props.id,
                    response: { confirmed: false },
                });
            }
        };

    Registries.Component.extend(AbstractAwaitablePopup, CustomPopup);
});
