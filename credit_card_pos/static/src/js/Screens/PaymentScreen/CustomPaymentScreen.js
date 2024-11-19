odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { useListener } = require("@web/core/utils/hooks");  // Importamos useListener

    const { removeEventListener, addEventListener } = owl;

    // Se añade la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        removeEventListener(window, "keyup", this._onKeyboardInput.bind(this)); // Elimina el listener del teclado
    };

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
                this._initializeListeners();
            }

            // Usamos useListener para agregar y eliminar el listener cuando los popups se abren y cierran
            _initializeListeners() {
                useListener("popup_opened", this._onPopupOpened);
                useListener("popup_closed", this._onPopupClosed);
            }

            // Función para manejar el evento cuando el popup se abre
            _onPopupOpened() {
                NumberBuffer.activate();  // Activamos el buffer de números
            }

            // Función para manejar el evento cuando el popup se cierra
            _onPopupClosed() {
                NumberBuffer.deactivate();  // Desactivamos el buffer de números
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

});
