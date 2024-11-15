odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { useExternalListener } = owl;

     // Añadir el método deactivate al prototipo de NumberBuffer
     NumberBuffer.prototype.deactivate = function () {
        // Eliminar el listener del teclado si está presente
        if (this.listenerAttached) {
            useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), true);
            this.listenerAttached = false;
        }
    };

    return NumberBuffer;
});
