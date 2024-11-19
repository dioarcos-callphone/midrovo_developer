odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup();

                // Vincular activación/desactivación dinámica
                NumberBuffer.use(() => {
                    if (this.isPopupOpen) {
                        this.deactivateNumberBuffer();
                    } else {
                        this.activateNumberBuffer();
                    }
                });
            }

            /**
             * Desactiva los eventos de teclado en NumberBuffer
             */
            deactivateNumberBuffer() {
                if (!this._keyboardListener) return; // Ya desactivado
                window.removeEventListener("keyup", this._keyboardListener);
                this._keyboardListener = null;
            }

            /**
             * Activa los eventos de teclado en NumberBuffer
             */
            activateNumberBuffer() {
                if (!this._onKeyboardInput) {
                    console.error("Método _onKeyboardInput no está definido.");
                    return;
                }
                if (this._keyboardListener) return; // Ya activado
                this._keyboardListener = this._onKeyboardInput.bind(this);
                window.addEventListener("keyup", this._keyboardListener);
            }
            

            /**
             * Sobrescribe `addNewPaymentLine` para manejar lógica de popups
             */
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

                    // Formatear las opciones de tarjeta para el popup
                    const cardOptions = getCards.map((card) => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    // Desactivar NumberBuffer antes de mostrar el popup
                    this.isPopupOpen = true;
                    this.deactivateNumberBuffer();

                    // Mostrar popup de selección de tarjeta
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        // Mostrar popup adicional de recap y autorización
                        const { confirmed: confirmedRecap, payload } = await this.showPopup(
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

                        if (confirmedRecap) {
                            const { recap, autorizacion, referencia } = payload;

                            let credit_card = {
                                card: selectedCreditCard,
                                recap: recap,
                                auth: autorizacion,
                                ref: referencia,
                            };

                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            // Añadir datos de tarjeta a la línea de pago
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            // Reactivar NumberBuffer después de procesar los popups
                            this.isPopupOpen = false;
                            this.activateNumberBuffer();

                            return result;
                        }
                    }

                    // Reactivar NumberBuffer si se cancela el popup
                    this.isPopupOpen = false;
                    this.activateNumberBuffer();
                } else {
                    // Manejo normal si no es tarjeta
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
