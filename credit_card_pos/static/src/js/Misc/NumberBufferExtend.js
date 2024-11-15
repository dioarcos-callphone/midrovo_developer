odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { removeExternalListener } = owl;

    // Extiende la clase NumberBuffer
    class NumberBufferExtend extends NumberBuffer {
        deactivate() {
            // Eliminar el listener de 'keyup'
            removeExternalListener(window, "keyup", this._onKeyboardInput.bind(this));
        }
    }

    // Exportar la clase extendida como default
    return new NumberBufferExtend();
});
