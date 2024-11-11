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
                // Llamamos al método original de PaymentScreen utilizando super
                const result = super.addNewPaymentLine({ detail: paymentMethod });
                
                // Aquí puedes agregar lógica adicional, si es necesario
                if (result) {
                    console.log("Pago agregado exitosamente");
                    return true;
                } else {
                    console.log("Error al agregar el pago");
                    return false;
                }
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
