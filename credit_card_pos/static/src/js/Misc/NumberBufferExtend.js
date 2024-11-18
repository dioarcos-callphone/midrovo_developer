odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { useExternalListener } = owl;

    // Guardamos la función de evento fuera para reutilizarla
    NumberBuffer._onKeyboardInput = NumberBuffer._onKeyboardInput;

    // Modificamos la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        this.defaultDecimalPoint = null; // Limpia el valor predeterminado
        useExternalListener(window, "keyup", null); // Elimina el listener del teclado
    };

    return NumberBuffer;
});
