/** @odoo-module **/

import PaymentScreen from "@point_of_sale/js/Screens/PaymentScreen/PaymentScreen";
import Registries from "@point_of_sale/js/Registries";

// Heredamos la clase PaymentScreen
const CustomPaymentScreen = (PaymentScreen) =>
    class extends PaymentScreen {
        // Extiende la función setup si quieres añadir lógica adicional
        setup() {
            super.setup();  // Llamar al método padre
        }
        
        mounted() {
            super.mounted();
            console.log("CustomPaymentScreen Mounted");
        }

    };

// Registramos la nueva clase heredada en los registros de Odoo
Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
