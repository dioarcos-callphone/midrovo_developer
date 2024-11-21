odoo.define("credit_card_pos.PosGlobalStateExtend", (require) => {
    "use strict";

    const { PosGlobalState, Payment } = require("point_of_sale.models");
    const Registries = require('point_of_sale.Registries');
    const rpc = require('web.rpc');

    const PosGlobalStateExtend = (PosGlobalState) => class PosGlobalStateExtend extends PosGlobalState {

        // Cargar datos persistidos de tarjetas de crédito al iniciar
        async _processData(loadedData) {
            await super._processData(...arguments);
            // Cargar tarjetas de crédito desde almacenamiento local si existen
            const storedCreditCard = localStorage.getItem("credit_card");
            if (storedCreditCard) {
                this.credit_card = JSON.parse(storedCreditCard);
            }
            this.credit_card_info = loadedData['credit.card.info'];
        }
        
        // Guardar datos de tarjetas de crédito cuando se guardan en el servidor
        async _save_to_server(orders, options) {
            const result = await super._save_to_server(orders, options);
            // Guardar las tarjetas de crédito en almacenamiento local
            localStorage.setItem("credit_card", JSON.stringify(this.credit_card));
            return result;
        }
    }

    // Extendemos la clase Payment para manejar la tarjeta de crédito
    const PaymentExtend = (Payment) => class PaymentExtend extends Payment {
        export_as_JSON() {
            const result = super.export_as_JSON();
            // Aseguramos que la tarjeta de crédito esté exportada en la transacción
            result.creditCard = this.creditCard;
            return result;
        }
    }

    Registries.Model.extend(PosGlobalState, PosGlobalStateExtend);
    Registries.Model.extend(Payment, PaymentExtend);
});
