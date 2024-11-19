odoo.define("credit_card_pos.CustomPopup", (require) => {
    "use strict";

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const { Registries } = require("point_of_sale.Registries");

    // Verificamos que AbstractAwaitablePopup esté registrado
    Registries.Component.add(AbstractAwaitablePopup);

    // Extender el AbstractAwaitablePopup
    const CustomPopup = AbstractAwaitablePopup =>
        class extends AbstractAwaitablePopup {
            mounted() {
                super.mounted();
                // Emitimos el evento cuando el popup se muestra
                this.trigger("show-popup", { popupId: this.props.id });
            }

            willUnmount() {
                // Emitimos el evento cuando el popup se cierra
                this.trigger("close-popup", { popupId: this.props.id });
                super.willUnmount();
            }

            async confirm() {
                // Confirmación personalizada antes de llamar a la lógica base
                await super.confirm();
                this.env.posbus.trigger("close-popup", {
                    popupId: this.props.id,
                    response: { confirmed: true },
                });
            }

            cancel() {
                // Cancelación personalizada antes de llamar a la lógica base
                super.cancel();
                this.env.posbus.trigger("close-popup", {
                    popupId: this.props.id,
                    response: { confirmed: false },
                });
            }
        };

    // Registrar el componente extendido en el registro de Odoo
    Registries.Component.extend(AbstractAwaitablePopup, CustomPopup);
});
