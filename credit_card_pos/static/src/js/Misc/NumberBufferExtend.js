odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Guardar los métodos originales
    const originalDeactivate = NumberBuffer.deactivate;

    // Sobrescribir deactivate
    NumberBuffer.deactivate = function () {
        // Llamar al método original
        if (originalDeactivate) {
            originalDeactivate.call(this);
        }

        // Eliminar el listener
        window.removeEventListener("keyup", this._onKeyboardInput.bind(this));
        this.listenerAttached = false;
    };

    return NumberBuffer;
});
