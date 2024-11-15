odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Sobrescribimos el método 'activate' de NumberBuffer
    NumberBuffer.activate = function () {
        // Llamamos al método original si es necesario
        this._super();

        // Aquí añades tu lógica personalizada
        console.log("NumberBuffer activate ha sido llamado");
        
        // Puedes agregar más lógica o condiciones si es necesario
    };

    return NumberBuffer;
});
