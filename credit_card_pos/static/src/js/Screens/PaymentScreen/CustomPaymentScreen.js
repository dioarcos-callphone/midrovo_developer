odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer"); // Importar NumberBuffer

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar al método padre
                this.isPopupActive = false; // Inicializa la bandera para saber si un popup está activo
            }

            _getNumberBufferConfig() {
                const config = super._getNumberBufferConfig(); // Llamamos al método original para obtener la configuración predeterminada

                // Agregar configuraciones adicionales si es necesario
                config.nonKeyboardInputEvent = "input-from-numpad"; // Usamos un evento no relacionado con el teclado si es necesario
                config.triggerAtInput = "update-selected-paymentline"; // Evento para actualizar la línea de pago

                return config;
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

                    // Mostramos el popup para seleccionar la tarjeta
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        this.isPopupActive = true; // El popup está activo, así que activamos la bandera

                        // Mostramos el segundo popup para los detalles de la tarjeta
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

                            // Llamamos al método original de PaymentScreen para agregar la línea de pago
                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            // Añadir credit_card en la línea de pago correspondiente
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            // Después de agregar la línea de pago, restablecemos el NumberBuffer
                            this._resetNumberBuffer();

                            return result;
                        }
                    }

                } else {
                    // Si no es una tarjeta, simplemente llamamos al método original
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }

            // Método para restablecer el NumberBuffer después de cerrar el popup
            _resetNumberBuffer() {
                this.isPopupActive = false; // Restablecer la bandera del popup

                // Llamamos a NumberBuffer.use para restablecer la configuración del buffer
                NumberBuffer.use(this._getNumberBufferConfig());
            }
        };

    // Registramos la clase modificada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
