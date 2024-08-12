odoo.define('pos_receipt_add_fields.pos_order', function (require) {
"use strict";

const { batched, uuidv4 } = require("point_of_sale.utils");

var { PosGlobalState, Order} = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
var rpc = require('web.rpc')
var Widget = require('web.Widget');

const PosSessionOrdersPosGlobalState = (PosGlobalState) => 
    class PosSessionOrdersPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
                //this.session_orders = loadedData['res.config.settings'];
                
                var receipt_number = this.env.pos.selectedOrder;
                //console.log('this.session_orders');
                //console.log(this.session_orders)
                //const options = {pos:this};
                //this.pos = options.pos;
                
        }
    } 

    Registries.Model.extend(PosGlobalState, PosSessionOrdersPosGlobalState);
    
});

