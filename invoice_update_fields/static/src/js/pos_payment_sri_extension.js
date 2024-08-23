odoo.define('invoice_update_fields.pos_payment_sri_extension', function(require) {
    "use strict";

    var { Order } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    var Widget = require("web.Widget");

    const PosPaymentSriOrder = (Order) =>  
        class PosPaymentSriOrder extends Order {
            //@override
            export_as_JSON() {
                const json = super.export_as_JSON(...arguments);
                this.get_l10n_ec_sri_payment_ids();
                json.l10n_ec_sri_payment_ids = this.get_l10n_ec_sri_payment_ids();
                return json;
            } 

            get_l10n_ec_sri_payment_ids() {
                let get_payment_sri = [];
                let paymentLines = this.get_paymentlines();
                if( paymentLines ){
                    paymentLines.forEach(paymentLine => {
                        get_payment_sri.push( {
                            payment_valor: paymentLine.amount,
                            l10n_ec_sri_payment_id: paymentLine.payment_method.l10n_ec_sri_payment_id[0]
                            ,
                        })
                    }); 
                }

                console.log(get_payment_sri)

                return  get_payment_sri;
            } 

    }

    Registries.Model.extend(Order, PosPaymentSriOrder);

});