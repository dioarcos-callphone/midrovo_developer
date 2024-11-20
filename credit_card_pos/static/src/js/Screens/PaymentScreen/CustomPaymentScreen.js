odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Modificar NumberBuffer para asegurar que los listeners se manejan dentro del ciclo de vida adecuado
    NumberBuffer.deactivate = function () {
        if (this._onKeyboardInput) {
            window.removeEventListener("keyup", null); // Elimina el listener del teclado
        }
    };

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar al método padre

                const bus = this.env.bus;

                // Registrar eventos globales
                // bus.on("deactivate", this, this._deactivate);
                // bus.on("activate", this, this._activate);
            }
    
            // Método _activate llamado dentro de un contexto adecuado (setup)
            _activate() {
                console.log("Activando el teclado numérico...");
                NumberBuffer.activate(); // Activar el teclado numérico
            }
    
            // Método _deactivate llamado dentro de un contexto adecuado (setup)
            _deactivate() {
                console.log("Desactivando el teclado numérico...");
                NumberBuffer.deactivate(); // Desactivar el teclado numérico
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

                    // Desactivamos el teclado numérico antes de mostrar el popup
                    // this._deactivate();
                    // this.env.bus.trigger("deactivate")

                    window.addEventListener('keyup', function(event) {
                        event.preventDefault();  // Prevenir el comportamiento predeterminado
                        event.stopPropagation(); // Evitar la propagación
                    
                        // Comprobamos si estamos en un campo de entrada (input o textarea)
                        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                            event.target.blur(); // Quitar el foco del campo de entrada
                        }
                    
                        console.log('Tecla liberada pero no se muestra el texto');
                    });
                    // Mostramos el popup para seleccionar la tarjeta
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        // Mostramos el segundo popup para los detalles de la tarjeta
                        const { confirmed, payload } = await this.showPopup("RecapAuthPopup", {
                            title: this.env._t(selectedCreditCard.name),
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

                            // Reactivar el teclado numérico después de la operación
                            // this._activate();

                            return result;
                        }

                        // this._activate();
                    }

                    // this._activate(); // Reactivar teclado después de mostrar el popup

                } else {
                    // Si no es una tarjeta, simplemente llamamos al método original
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };

    // Registramos la clase modificada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
