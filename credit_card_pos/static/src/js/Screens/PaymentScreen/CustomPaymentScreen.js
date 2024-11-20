odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Se añade la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        window.removeEventListener("keyup", this._onKeyboardInput.bind(this)); // Elimina el listener del teclado
    };

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar al método padre

                // Usa el bus global desde el entorno
                const bus = this.env.bus;

                // Usar NumberBuffer en el contexto de setup
                NumberBuffer.use(() => {
                    // Registrar eventos globales
                    bus.on("deactivate", this, () => {
                        this._deactivate();
                    });
                    bus.on("activate", this, () => {
                        this._activate();
                    });
                });
            }
    
            _activate() {
                console.log("ENTRA EN ACTIVATE");
                NumberBuffer.activate(); // Activar el teclado numérico
            }
    
            _deactivate() {
                console.log("ENTRA EN DEACTIVATE");
                NumberBuffer.deactivate(); // Desactivar el teclado numérico
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

                    // Desactivamos el evento de teclado en el popup abierto
                    this.env.bus.trigger("deactivate");

                    // Mostramos el primer popup para selección de tarjeta
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup", // Usamos el popup correcto para selección de lista
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        // Mostramos el segundo popup para los detalles de la tarjeta
                        const { confirmed, payload } = await this.showPopup("RecapAuthPopup", {
                            title: this.env._t(selectedCreditCard.name), // Título del popup
                            recapPlaceholder: this.env._t("Ingrese RECAP"), // Placeholder para el campo RECAP
                            autorizacionPlaceholder: this.env._t("Ingrese Autorización"), // Placeholder para el campo Autorización
                            referenciaPlaceholder: this.env._t("Ingrese Referencia"), // Placeholder para el campo Referencia
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

                            // Aquí se añade en el diccionario la llave creditCard para almacenar los valores
                            // que se encuentran en la variable credit_card
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            // this.env.bus.trigger("activate");

                            return result;
                        }

                        // this.env.bus.trigger("activate");
                    }

                    // this.env.bus.trigger("activate");

                } else {
                    // Si no es una tarjeta, simplemente llamamos al método original
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
