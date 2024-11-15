odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Guardar los métodos originales
    const originalActivate = NumberBuffer.activate;
    const originalDeactivate = NumberBuffer.deactivate;

    // Sobrescribir activate
    NumberBuffer.activate = function () {
        // Llamar al método original
        if (originalActivate) {
            originalActivate.call(this);
        }

        // Agregar lógica adicional
        if (!this.listenerAttached) {
            window.addEventListener("keyup", this._onKeyboardInput.bind(this));
            this.listenerAttached = true;
        }
    };

    // Sobrescribir deactivate
    NumberBuffer.deactivate = function () {
        // Llamar al método original
        if (originalDeactivate) {
            originalDeactivate.call(this);
        }

        // Eliminar el listener
        if (this.listenerAttached) {
            window.removeEventListener("keyup", this._onKeyboardInput.bind(this));
            this.listenerAttached = false;
        }
    };

    return NumberBuffer;
});
