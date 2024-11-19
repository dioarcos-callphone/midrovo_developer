odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const { removeEventListener, addEventListener } = owl;

    // Añadir la función deactivate y asegurar la activación al salir
    NumberBuffer.deactivate = function () {
        removeEventListener(window, "keyup", this._onKeyboardInput.bind(this)); // Elimina el listener del teclado
    };

    NumberBuffer.activate = function () {
        addEventListener(window, "keyup", this._onKeyboardInput.bind(this)); // Vuelve a añadir el listener del teclado
    };

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async addNewPaymentLine({ detail: paymentMethod }) {
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

                    // Desactivar el evento del teclado antes de mostrar el popup
                    NumberBuffer.deactivate();

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

                            // Reactivar el evento del teclado después del popup
                            NumberBuffer.activate();

                            return result;
                        }
                    }

                    // Reactivar el evento del teclado si se cierra el popup sin confirmar
                    NumberBuffer.activate();
                } else {
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
