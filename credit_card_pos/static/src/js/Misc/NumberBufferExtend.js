odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Modificamos la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        window.removeEventListener("keyup", this._onKeyboardInput.bind(this), false); // Elimina el listener del teclado
    };

    return NumberBuffer;
});
