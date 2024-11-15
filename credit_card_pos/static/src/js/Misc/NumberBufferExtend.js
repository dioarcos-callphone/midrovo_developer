odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Sobrescribir deactivate
    NumberBuffer.deactivate = function (event) {
        // Eliminar el listener
        event.preventDefault();
        event.stopPropagation();
    };

    return NumberBuffer;
});
