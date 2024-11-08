/** @odoo-module **/

import PaymentScreen from "@point_of_sale/js/Screens/PaymentScreen/PaymentScreen";
import Registries from "@point_of_sale/js/Registries";

// Heredamos la clase PaymentScreen
const CustomPaymentScreen = (PaymentScreen) =>
    class extends PaymentScreen {
        // Extiende la función setup si quieres añadir lógica adicional
        setup() {
            super.setup();  // Llamar al método padre
            // Añade o modifica comportamiento aquí
            console.log("Bienvenido a la pantalla de Pagos");
        }

    };

// Registramos la nueva clase heredada en los registros de Odoo
Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
