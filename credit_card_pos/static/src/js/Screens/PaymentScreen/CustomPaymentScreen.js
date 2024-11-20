odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const { onMounted } = owl;

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar al método padre
            }

            // Sobrescribir el getter _getNumberBufferConfig
            get _getNumberBufferConfig() {
                const config = super._getNumberBufferConfig;

                this.env.bus.on("desactivar", this, () => {
                    console.log("desactivamos triggerAtInput")
                    config.triggerAtInput = ""
                })

                this.env.bus.on("activar", this, () => {
                    console.log("activamos triggerAtInput")
                    config.triggerAtInput = "update-selected-paymentline"
                })

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
                    this.env.bus.trigger("desactivar");
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

                            this.env.bus.trigger("activar");
                            return result;
                        }
                    }
            
                } else {
                    // Si no es una tarjeta, simplemente llamamos al método original
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
            
        };

    // Registramos la clase modificada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
