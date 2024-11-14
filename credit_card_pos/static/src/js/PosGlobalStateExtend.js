odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState, Payment } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        async _save_to_server(orders, options) {
            const creditCards = this.env.pos.creditCards || [];
            // SE OBTIENE DICCIONARIO EJ. {id: 865, pos_reference: 'Pedido 00142-356-0001', account_move: 1951}
            const result = await super._save_to_server(orders, options);

            // const statement_ids = orders.map(order => order.data.statement_ids);
            // const statements = this.getStatements(statement_ids);

            const data = orders.map(order => order.data);
            const statement_ids = data.map(d => d.statement_ids);
            const statements = data.map(statement => {
                console.log('MOSTRANDO STATMENT')
                console.log(statement)
            })

            if(statements) {
                // console.log(statements)

                // await rpc.query({
                //     model: 'pos.payment',
                //     method: 'update_invoice_payments_widget',
                //     args: [ creditCards, result ]
                // })

                // Limpiamos la lista de tarjetas de crédito después de enviarlas
                this.env.pos.creditCards = [];

            }

            return result
        }

        getStatements(statement_ids) {
            // Extraer los valores de amount, creditCard, y payment_method_id, filtrando donde creditCard no sea undefined
            const extractedData = statement_ids.map(statement => {
                const st = statement
                    .map(s => {
                        const obj = s[2]; // El objeto está en el índice 2 de cada sub-array
                        return {
                            amount: obj.amount,
                            creditCard: obj.creditCard,
                            payment_method_id: obj.payment_method_id
                        };
                    })
                    .filter(item => item.creditCard !== undefined); // Filtrar donde creditCard no es undefined
                return st;
            });

            //const creditCards = extractedData.filter(item => item.creditCard);

            // console.log(creditCards);

            return extractedData
        }
    }

    // Extendemos la clase Payment para obtener el creditCard que viene del paymentLines
    const PaymentExtend = (Payment) => class PaymentExtend extends Payment {
        export_as_JSON() {

            const result = super.export_as_JSON();
            result.creditCard = this.creditCard
            return result;
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);
    Registries.Model.extend(Payment, PaymentExtend);



});
