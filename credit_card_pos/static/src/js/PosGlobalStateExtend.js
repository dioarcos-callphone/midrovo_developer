odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState, Payment } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {
            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);
            
            console.log(this.env.pos);
            
            const data = orders.map(order => order.data);
            const statement_ids = data.map(d => d.statement_ids);
            
            const statements = statement_ids.map(statement => {
                return statement.filter(item => item[2].creditCard !== undefined)
            });

            const statementCreditCards = statements.map(statement => {
                return statement.map(item => {
                    const obj = item[2];
                    return {
                        amount: obj.amount,
                        creditCard: obj.creditCard,
                        payment_method_id: obj.payment_method_id,
                    }
                });
            });

            let isContent = false;

            for(const statementCreditCard of statementCreditCards) {
                if(statementCreditCard.length > 0) {
                    isContent = true
                    break;
                }
            }

            if(isContent) {
                const statementFlated = statementCreditCards.flat();
                await rpc.query({
                    model: 'pos.payment',
                    method: 'update_invoice_payments_widget',
                    args: [ statementFlated, result ]
                });

            }

            return result
        }

    }

    // Extendemos la clase Payment para obtener el creditCard que viene del paymentLines
    const PaymentExtend = (Payment) => class PaymentExtend extends Payment {
        export_as_JSON() {
            console.log(this.creditCard)
            const result = super.export_as_JSON();
            result.creditCard = this.creditCard

            return result;
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);
    Registries.Model.extend(Payment, PaymentExtend);

});
