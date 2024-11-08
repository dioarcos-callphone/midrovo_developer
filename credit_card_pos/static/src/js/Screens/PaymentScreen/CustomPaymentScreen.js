odoo.define("credit_card_pos.CustomPaymentScreen", (require) => {
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    // Heredamos la clase PaymentScreen
    const CustomPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            // Extiende la función setup si quieres añadir lógica adicional
            setup() {
                super.setup();  // Llamar al método padre
                console.log("CustomPaymentScreen Setup");
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
