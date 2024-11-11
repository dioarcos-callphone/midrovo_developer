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
            addNewPaymentLine({ detail: paymentMethod }) {
                console.log("MOSTRANDO PAYMENT METHOD")
                console.log(paymentMethod)

                // Retornamos el método original de PaymentScreen utilizando super
                return super.addNewPaymentLine({ detail: paymentMethod });
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
