odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const { useExternalListener } = require("web.core");

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
                this._isPopupOpen = false;  // Estado para controlar si el popup está abierto
            }

            // Sobrescribimos el método addNewPaymentLine
            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name

                const isCard = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [ method_name ],
                });

                if(isCard) {
                    const getCards = await this.rpc({
                        model: "credit.card",
                        method: "get_cards",
                    });

                    const cardOptions = getCards.map(card => ({
                        id: card.id,
                        label: card.name,
                        item: card.name,
                    }));

                    // Deshabilitar la escucha del teclado cuando se muestra el popup
                    this._disableKeyboardListener();

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
                            }

                            const result = super.addNewPaymentLine({ detail: paymentMethod });

                            // Actualizamos el pago con la información de la tarjeta
                            for(let p of this.paymentLines) {
                                if(!p.creditCard && paymentMethod.id === p.payment_method.id) {
                                    p.creditCard = credit_card;
                                }
                            }

                            return result;
                        }

                    }

                } else {
                    // Retornamos el método original de PaymentScreen utilizando super
                    return super.addNewPaymentLine({ detail: paymentMethod });
                }
            }

            // Deshabilita el evento global de teclado cuando un popup está abierto
            _disableKeyboardListener() {
                if (!this._isPopupOpen) {
                    useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), false);
                    this._isPopupOpen = true;
                }
            }

            // Habilita el evento global de teclado después de que el popup se cierre
            _enableKeyboardListener() {
                if (this._isPopupOpen) {
                    useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), true);
                    this._isPopupOpen = false;
                }
            }
        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
});
