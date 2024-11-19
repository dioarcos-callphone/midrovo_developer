odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const { useBus } = require("web.core");

    let isKeyupDisabled = false; // Flag para habilitar/deshabilitar el evento

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup();
                
                // Registrar el evento keyup en el bus global
                this.env.bus.on("keyup", this, this.handleKeyup);
            }

            // Manejo personalizado del evento keyup
            handleKeyup(event) {
                if (isKeyupDisabled) {
                    console.log("Evento keyup desactivado.");
                    return; // No hacemos nada si está deshabilitado
                }
                console.log("Evento keyup activado:", event.key);
                // Aquí puedes agregar lógica adicional según la tecla presionada
            }

            // Método para desactivar el evento keyup
            disableKeyup() {
                isKeyupDisabled = true;
            }

            // Método para activar nuevamente el evento keyup
            enableKeyup() {
                isKeyupDisabled = false;
            }

            async addNewPaymentLine({ detail: paymentMethod }) {
                // Desactivar el evento keyup antes de mostrar los popups
                this.disableKeyup();

                const method_name = paymentMethod.name;

                const isCard = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [method_name],
                });

                if (isCard) {
                    const getCards = await this.rpc({
                        model: "credit.card",
                        method: "get_cards",
                    });

                    const cardOptions = getCards.map((card) => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        const { confirmed, payload } = await this.showPopup(
                            "RecapAuthPopup",
                            {
                                title: this.env._t(selectedCreditCard),
                                recapPlaceholder: this.env._t("Ingrese RECAP"),
                                autorizacionPlaceholder: this.env._t("Ingrese Autorización"),
                                referenciaPlaceholder: this.env._t("Ingrese Referencia"),
                                startingRecapValue: "",
                                startingAutorizacionValue: "",
                                startingReferenciaValue: "",
                            }
                        );

                        if (confirmed) {
                            const { recap, autorizacion, referencia } = payload;

                            let credit_card = {
                                card: selectedCreditCard,
                                recap: recap,
                                auth: autorizacion,
                                ref: referencia,
                            };

                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            // Reactivar el evento keyup después de la lógica
                            this.enableKeyup();
                            return result;
                        }
                    }
                } else {
                    const result = super.addNewPaymentLine({ detail: paymentMethod });
                    this.enableKeyup(); // Reactivar el evento keyup
                    return result;
                }

                // Reactivar el evento keyup si no se entra en ninguna condición previa
                this.enableKeyup();
            }

            // Limpiar el evento al destruir el componente
            willUnmount() {
                super.willUnmount();
                this.env.bus.off("keyup", this, this.handleKeyup);
            }
        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
