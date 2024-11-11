odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");
    // const { useState } = require("owl");

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
                // this.state = useState({ showModal: false }); // Estado para controlar el modal
            }

            // Sobrescribimos el método addNewPaymentLine
            async addNewPaymentLine({ detail: paymentMethod }) {
                const method_name = paymentMethod.name

                const result_rpc = await this.rpc({
                    model: "pos.payment.method",
                    method: "is_card",
                    args: [ method_name ]
                })

                if(result_rpc) {
                    // Si el resultado del RPC es true, mostramos el modal
                    const { confirmed, payload: selectedCreditCard } = await this.showPopup(
                        "SelectionPopup",
                        {
                            title: this.env._t("Seleccione la Tarjeta de Credito"),
                            list: ['Visa', 'MasterCard', 'Dinners Club'],
                        }
                    );

                    if (confirmed) {
                        console.log(selectedCreditCard)
                    }
                }

                // Retornamos el método original de PaymentScreen utilizando super
                return super.addNewPaymentLine({ detail: paymentMethod });
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
