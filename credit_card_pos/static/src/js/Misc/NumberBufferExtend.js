odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    NumberBuffer.deactivate = function () {
        window.removeEventListener("keyup", this._onKeyboardInput); // Elimina el listener del teclado
    };

    return NumberBuffer;
});
