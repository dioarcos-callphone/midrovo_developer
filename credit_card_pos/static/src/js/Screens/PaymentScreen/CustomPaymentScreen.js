odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const { onMounted, onWillUnmount } = owl;

    // Extendemos el PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
                this.keyboardActive = true; // Control interno del estado del teclado

                // Monitorizar el estado de desactivación
                onMounted(() => {
                    if (!this.keyboardActive) {
                        this.deactivateKeyboard();
                    }
                });

                onWillUnmount(() => {
                    if (!this.keyboardActive) {
                        this.activateKeyboard();
                    }
                });
            }

            // Desactiva el evento del teclado
            deactivateKeyboard() {
                NumberBuffer.removeListeners();
                this.keyboardActive = false;
            }

            // Activa el evento del teclado
            activateKeyboard() {
                NumberBuffer.addListeners();
                this.keyboardActive = true;
            }

            // Sobrescribir el método addNewPaymentLine
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

                    // Formatear las tarjetas para el popup
                    const cardOptions = getCards.map((card) => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    this.deactivateKeyboard(); // Desactiva el teclado antes de abrir el popup

                    // Mostrar el popup de selección de tarjeta
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        const { confirmed, payload } = await this.showPopup("RecapAuthPopup", {
                            title: this.env._t(selectedCreditCard), // Título del popup
                            recapPlaceholder: this.env._t("Ingrese RECAP"),
                            autorizacionPlaceholder: this.env._t("Ingrese Autorización"),
                            referenciaPlaceholder: this.env._t("Ingrese Referencia"),
                            startingRecapValue: "",
                            startingAutorizacionValue: "",
                            startingReferenciaValue: "",
                        });

                        if (confirmed) {
                            const { recap, autorizacion, referencia } = payload;

                            const credit_card = {
                                card: selectedCreditCard,
                                recap: recap,
                                auth: autorizacion,
                                ref: referencia,
                            };

                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            // Asociar los datos de la tarjeta al pago correspondiente
                            for (let p of this.paymentLines) {
                                if (
                                    !p.creditCard &&
                                    paymentMethod.id === p.payment_method.id
                                ) {
                                    p.creditCard = credit_card;
                                }
                            }

                            this.activateKeyboard(); // Reactiva el teclado tras el popup
                            return result;
                        }
                    }

                    this.activateKeyboard(); // Reactiva el teclado si el popup se cancela
                } else {
                    // Método original si no se utiliza tarjeta
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    // Registramos la nueva clase en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
