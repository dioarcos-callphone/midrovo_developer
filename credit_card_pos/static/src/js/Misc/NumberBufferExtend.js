odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { useExternalListener } = owl;

    // Usar una función tradicional para preservar el contexto de `this`
    NumberBuffer.deactivate = function () {
        if (this.listenerAttached) {
            // Eliminar el listener de teclado si está presente
            useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), true);
            this.listenerAttached = false;
        }
    }

    NumberBuffer.activate = function () {
        // Llamar al método original de NumberBuffer.activate()
        if (!this.listenerAttached) {
            // Llamamos a la implementación original de activate de NumberBuffer
            this.activate.call(this); // Esto llama al método original

            this.listenerAttached = true;
        }
    };

    return NumberBuffer;
});
