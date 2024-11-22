odoo.define("credit_card_info.db", (require) => {
    const PosDB = require("point_of_sale.DB")

    PosDB.include({
        init: function (options) {
            this._super(options);
            this.paymentLineCreditCards = {};
        },
    
        save_payment_line_credit_card: function (paymentLineId, creditCardInfo) {
            this.paymentLineCreditCards[paymentLineId] = creditCardInfo;
        },
    
        get_payment_line_credit_card: function (paymentLineId) {
            return this.paymentLineCreditCards[paymentLineId];
        },
    
        remove_payment_line_credit_card: function (paymentLineId) {
            delete this.paymentLineCreditCards[paymentLineId];
        },
    });

    return PosDB
})