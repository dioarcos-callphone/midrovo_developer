odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Usar una función tradicional para preservar el contexto de `this`
    NumberBuffer.deactivate = function () {
        // Eliminar el listener de 'keyup'
        window.removeEventListener("keyup", this._onKeyboardInput);
    }

    return NumberBuffer;
});
