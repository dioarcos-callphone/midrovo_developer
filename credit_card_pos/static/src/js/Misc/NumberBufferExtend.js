odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { removeEventListener } = owl;

    // Guardamos la función de evento fuera para reutilizarla
    NumberBuffer._onKeyboardInput = NumberBuffer._onKeyboardInput;

    // Se añade la función deactivate para eliminar el listener
    NumberBuffer.deactivate = function () {
        removeEventListener(window, "keyup", this._onKeyboardInput.bind(this)); // Elimina el listener del teclado
    };

    return NumberBuffer;

});
