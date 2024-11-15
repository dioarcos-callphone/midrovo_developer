odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Sobrescribimos el método 'deactivate' de NumberBuffer
    NumberBuffer.deactivate = function () {
        // Elimina el listener de 'keyup' para que no escuche las teclas presionadas
        useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), false);
        
        console.log("NumberBuffer deactivate ha sido llamado");
    };

    return NumberBuffer;
});
