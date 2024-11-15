odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Guardamos una referencia al método original
    const originalActivate = NumberBuffer.activate;

    // Sobrescribimos el método 'activate' de NumberBuffer
    NumberBuffer.activate = function () {
        // Llamamos al método original
        if (originalActivate) {
            originalActivate.call(this); // Ejecutamos el método original
        }

        // Añadimos lógica adicional
        console.log("NumberBuffer activate ha sido llamado");

        // Puedes añadir más lógica si es necesario
    };

    return NumberBuffer;
});
