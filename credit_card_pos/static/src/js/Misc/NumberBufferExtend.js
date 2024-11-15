odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { useExternalListener } = owl;

    // Sobrescribir el método activate para agregar listenerAttached
    NumberBuffer.prototype.activate = function () {
        // Llamar al método original de NumberBuffer.activate()
        if (!this.listenerAttached) {
            // Llamamos a la implementación original de activate de NumberBuffer
            NumberBuffer.prototype.activate.call(this); // Esto llama al método original

            this.listenerAttached = true;
        }
    };

    // Añadir el método deactivate para eliminar el listener
    NumberBuffer.prototype.deactivate = function () {
        // Verificar si el listener está adjunto antes de intentar eliminarlo
        if (this.listenerAttached) {
            useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), true);
            this.listenerAttached = false;
        }
    };

    return NumberBuffer;
});
