odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // const { removeEventListener } = owl;

    // Se añade la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        window.removeEventListener("keyup", this._onKeyboardInput);
    };

    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            setup() {
                super.setup(); // Llamar a la configuración base de la clase padre
    
                // Aquí podrías agregar lógica adicional, si es necesario
                console.log("CustomPaymentScreen setup called");
            }
    
            // Funciones para manejar NumberBuffer
            deactivateNumberBuffer() {
                NumberBuffer.deactivate();
            }
    
            activateNumberBuffer() {
                NumberBuffer.activate();
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
    
                    this.deactivateNumberBuffer();
    
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
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
    
                        if (confirmed) {
                            const { recap, autorizacion, referencia } = payload;
    
                            let credit_card = {
                                card: selectedCreditCard,
                                recap: recap,
                                auth: autorizacion,
                                ref: referencia,
                            };
    
                            const result = super.addNewPaymentLine({ detail: paymentMethod });
    
                            for (let p of this.paymentLines) {
                                if (!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }
    
                            this.activateNumberBuffer();
                            return result;
                        }
                    }
    
                    this.activateNumberBuffer();
                } else {
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }
        };    

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
