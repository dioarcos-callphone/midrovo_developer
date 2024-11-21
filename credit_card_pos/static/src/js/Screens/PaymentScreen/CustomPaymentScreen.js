odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar al método padre
                this.isUpdateSelectedPaymentlineActive = true;
            }

            _updateSelectedPaymentline() {
                if (!this.isUpdateSelectedPaymentlineActive) {
                    NumberBuffer.reset();
                    return;
                }

                super._updateSelectedPaymentline()
                // Lógica original del método
            }
            
            // Métodos para activar/desactivar
            disableUpdateSelectedPaymentline() {
                this.isUpdateSelectedPaymentlineActive = false;
            }
            
            enableUpdateSelectedPaymentline() {
                this.isUpdateSelectedPaymentlineActive = true;
            }

            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name;
            
                const isCard = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [method_name],
                });
            
                if (isCard) {
                    // this.env.bus.trigger("desactivar");

                    this.disableUpdateSelectedPaymentline();
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

                            this.enableUpdateSelectedPaymentline();
                            return result;
                        }
                        this.enableUpdateSelectedPaymentline();
                    }
                    this.enableUpdateSelectedPaymentline();
            
                } else {
                    // Si no es una tarjeta, simplemente llamamos al método original
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
            
        };

    // Registramos la clase modificada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
