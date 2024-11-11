odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
            }

            // Sobrescribimos el método addNewPaymentLine
            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name

                const isCard = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [ method_name ]
                })

                if(isCard) {
                    const getCards = await this.rpc({
                        model: "credit.card",
                        method: "get_cards",
                    })

                    // Formatear las tarjetas para el popup
                    const cardOptions = getCards.map(card => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    // Si el resultado del RPC es true, mostramos el modal
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",  // Usamos el popup correcto para selección de lista
                        {
                            title: this.env._t("Seleccione la Tarjeta de Crédito"),
                            list: cardOptions,
                        }
                    );

                    if (confirmed) {
                        const { confirmed, payload } = await this.showPopup(
                            "RecapAuthPopup",
                            {
                                title: this.env._t(selectedCreditCard), // Título del popup
                                recapPlaceholder: this.env._t("Ingrese RECAP"), // Placeholder para el campo RECAP
                                autorizacionPlaceholder: this.env._t("Ingrese Autorización"), // Placeholder para el campo Autorización
                                startingRecapValue: "",
                                startingAutorizacionValue: "",
                            }
                        );
                        
                        if (confirmed) {
                            const { recap, autorizacion } = payload;
                            console.log("RECAP:", recap);
                            console.log("Autorización:", autorizacion);

                            return super.addNewPaymentLine({ detail: paymentMethod });
                        }


                    }
                }

                else {
                    // Retornamos el método original de PaymentScreen utilizando super
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }

            }

            async _finalizeValidation() {
                // Aquí agregamos la funcionalidad personalizada después de llamar al método original
                console.log("El proceso de validación se ha completado y se ha personalizado.");
                console.log(this.currentOrder)

                // Llamamos al método original con `super()`
                await super._finalizeValidation();

            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
