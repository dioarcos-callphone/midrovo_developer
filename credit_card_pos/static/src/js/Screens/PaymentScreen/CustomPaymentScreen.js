odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");

    // Extender el AbstractPopup para manejar el estado del teclado
    const CustomAbstractPopup = (AbstractAwaitablePopup) =>
        class extends AbstractAwaitablePopup {
            willStart() {
                // Antes de mostrar el popup, desactiva el teclado
                isPopupOpen = true;
                NumberBuffer.deactivate();
                return super.willStart();
            }

            willUnmount() {
                // Al cerrar el popup, reactiva el teclado
                isPopupOpen = false;
                NumberBuffer.activate();
                return super.willUnmount();
            }
        };
    Registries.Component.extend(AbstractAwaitablePopup, CustomAbstractPopup);

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre

                // Desactivamos el evento del teclado cuando se habilite el popup para las tarjetas de credito
                // NumberBuffer.use((control) => this.numberActivateToggle(control));

            }

            numberActivateToggle(control) {
                // if (typeof control === 'boolean') {
                //     control ? NumberBuffer.deactivate() : NumberBuffer.activate();
                // }
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
                    });

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
                                referenciaPlaceholder: this.env._t("Ingrese Referencia"), // Placeholder para el campo Referencia
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
                            }

                            const result = super.addNewPaymentLine({ detail: paymentMethod });
                            
                            // Aqui se añade en el diccionario la llave creditCard para almacenar los valores
                            // que se encuentran en la variable credit_card
                            for(let p of this.paymentLines) {
                                if(!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card
                                }
                            }
    
                            return result;
                        }

                    }

                }

                else {
                    // Retornamos el método original de PaymentScreen utilizando super
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }

            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
