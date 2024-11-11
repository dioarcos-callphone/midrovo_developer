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

            selectPaymentLine(event) {
                console.log("ENTRAMOS A SELECT PAYMENT LINE");
                const { cid } = event.detail;
                const line = this.paymentLines.find((line) => line.cid === cid);
                // Puedes agregar lógica adicional aquí si lo necesitas
                this.currentOrder.select_paymentline(line);
                NumberBuffer.reset();
                this.render(true);
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);

})
