odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const { useBus } = require("@web/core/utils/hooks");
    const { removeEventListener } = owl;

    // Se añade la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        removeEventListener(window, "keyup", this._onKeyboardInput.bind(this)); // Elimina el listener del teclado
    };

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup();
                // Escuchar eventos del Bus
                console.log("MOSTRANDO USE BUS");
                console.log(this.env.bus);
                console.log(useBus);
                useBus(this.env.bus, "modal:opened", () => this._onModalOpened());
                useBus(this.env.bus, "modal:closed", () => this._onModalClosed());
            }

            _onModalOpened() {
                // Desactivar el teclado
                NumberBuffer.deactivate();
            }

            _onModalClosed() {
                // Activar el teclado
                NumberBuffer.activate();
            }

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

                    // Emitir el evento de apertura de modal
                    this.bus.trigger("modal:opened");
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        const { confirmed, payload } = await this.showPopup("RecapAuthPopup", {
                            title: this.env._t(selectedCreditCard),
                            recapPlaceholder: this.env._t("Ingrese RECAP"),
                            autorizacionPlaceholder: this.env._t("Ingrese Autorización"),
                            referenciaPlaceholder: this.env._t("Ingrese Referencia"),
                            startingRecapValue: "",
                            startingAutorizacionValue: "",
                            startingReferenciaValue: "",
                        });

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

                            // Emitir el evento de cierre de modal
                            this.bus.trigger("modal:closed");
                            return result;
                        }
                    }

                    // Emitir el evento de cierre de modal si se cancela
                    this.bus.trigger("modal:closed");
                } else {
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
