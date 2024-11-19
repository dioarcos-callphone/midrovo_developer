odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Agregamos un método para desactivar el buffer temporalmente
    NumberBuffer.disableTemporary = function () {
        if (this._keyboardInputListener) {
            window.removeEventListener("keyup", this._onKeyboardInput.bind(this));
            this._keyboardInputListener = false; // Flag para indicar que el listener está deshabilitado
        }
    };

    // Agregamos un método para restaurar el buffer
    NumberBuffer.enableTemporary = function () {
        if (!this._keyboardInputListener) {
            window.addEventListener("keyup", this._onKeyboardInput.bind(this));
            this._keyboardInputListener = true; // Flag para indicar que el listener está activo
        }
    };

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup(); // Llamar al método padre
            }

            // Sobrescribimos el método addNewPaymentLine
            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name;

                const isCard = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [method_name],
                });

                if (isCard) {
                    // Desactivar temporalmente los eventos del teclado
                    NumberBuffer.disableTemporary();

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

                    // Mostrar el primer popup
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        // Mostrar el segundo popup
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

                            // Añadir la información de la tarjeta a la línea de pago
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            // Reactivar los eventos del teclado después de que el popup se cierre
                            NumberBuffer.enableTemporary();

                            return result;
                        }
                    }

                    // Reactivar los eventos del teclado si se cancela
                    NumberBuffer.enableTemporary();
                } else {
                    // Retornar el método original de PaymentScreen utilizando super
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
