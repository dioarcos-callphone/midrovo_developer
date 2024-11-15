odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { removeExternalListener } = owl;

    // Usar una función tradicional para preservar el contexto de `this`
    NumberBuffer.deactivate = function () {
        // Eliminar el listener de 'keyup'
        removeExternalListener(window, "keyup", this._onKeyboardInput.bind(this));
    }

    return NumberBuffer;
});
