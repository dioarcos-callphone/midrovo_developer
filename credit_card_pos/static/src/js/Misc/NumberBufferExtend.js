odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Sobrescribimos el método 'activate' de NumberBuffer
    NumberBuffer.deactivate = function () {
        useExternalListener(window, "keydown", this._onKeyboardInput.bind(this));
        console.log("NumberBuffer deactivate ha sido llamado");

        // Puedes añadir más lógica si es necesario
    };

    return NumberBuffer;
});
