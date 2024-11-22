odoo.define("credit_card_pos.CustomPaymentScreenPaymentLines", (require) => {
    const Registries = require("point_of_sale.Registries");
    const PaymentScreenPaymentLines = require("point_of_sale.PaymentScreenPaymentLines");

    const CustomPaymentScreenPaymentLines = (PaymentScreenPaymentLines) =>
        class extends PaymentScreenPaymentLines {
            formatLineAmount(paymentline) {
                console.log("ENTRAMOS EN EL PAYMENTLINES")
                console.log(this)
                console.log(paymentline);
                return super.formatLineAmount(paymentline);
            }
        }

    Registries.Component.extend(PaymentScreenPaymentLines, CustomPaymentScreenPaymentLines);

    return PaymentScreenPaymentLines;
});