odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Extendemos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Sobrescribimos la función setup si es necesario
            setup() {
                super.setup();  // Llamamos al método original
                // Usamos un evento del ciclo de vida para manejar el input del teclado
                this._bindKeyboardEvents();
            }

            // Método para manejar los eventos del teclado
            _bindKeyboardEvents() {
                if (this._onKeyboardInput) {
                    // Aseguramos que el evento se agrega correctamente
                    window.addEventListener("keyup", this._onKeyboardInput.bind(this));
                }
            }

            // Método para eliminar el listener cuando ya no se necesite
            _unbindKeyboardEvents() {
                if (this._onKeyboardInput) {
                    // Eliminamos el listener
                    window.removeEventListener("keyup", this._onKeyboardInput.bind(this));
                }
            }

            // Sobrescribimos la función addNewPaymentLine para interactuar con tarjetas
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

                    // Formateamos las tarjetas para mostrarlas en un popup
                    const cardOptions = getCards.map(card => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    // Desactivamos el input del teclado antes de mostrar el popup
                    NumberBuffer.deactivate();

                    // Si el usuario selecciona una tarjeta, procesamos el pago
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",  // Usamos el popup adecuado
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

                        // Reactivamos el input del teclado después de interactuar con el popup
                        NumberBuffer.activate();

                        if (confirmed) {
                            const { recap, autorizacion, referencia } = payload;

                            let credit_card = {
                                card: selectedCreditCard,
                                recap: recap,
                                auth: autorizacion,
                                ref: referencia,
                            };

                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            // Añadimos los datos de la tarjeta en la línea de pago
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            return result;
                        }
                    }
                } else {
                    // Si no es una tarjeta, llamamos al método original de PaymentScreen
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    // Registramos el componente extendido
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

});
