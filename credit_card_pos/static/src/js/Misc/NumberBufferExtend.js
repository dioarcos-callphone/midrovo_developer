odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Guardamos la función de evento fuera para reutilizarla
    NumberBuffer._onKeyboardInput = NumberBuffer._onKeyboardInput;

    // Modificamos la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        window.removeEventListener("keyup", NumberBuffer._onKeyboardInput.bind(this), false); // Elimina el listener del teclado
    };

    return NumberBuffer;
});
