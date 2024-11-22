odoo.define("credit_card_pos.CustomPaymentScreenPaymentLines", (require) => {
    const Registries = require("point_of_sale.Registries");
    const PaymentScreenPaymentLines = require("point_of_sale.PaymentScreenPaymentLines");

    const CustomPaymentScreenPaymentLines = (PaymentScreenPaymentLines) =>
        class extends PaymentScreenPaymentLines {
            selectedLineClass(line) {
                
                return super.selectedLineClass(line);
            }
        }

    Registries.Component.extend(PaymentScreenPaymentLines, CustomPaymentScreenPaymentLines);

    return PaymentScreenPaymentLines;
});