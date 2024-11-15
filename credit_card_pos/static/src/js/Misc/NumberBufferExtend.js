odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const { removeExternalListener } = owl;

    NumberBuffer.deactivate = async () => {
        // Eliminar el listener de 'keyup'
        removeExternalListener(window, "keyup", this._onKeyboardInput.bind(this));
    }

    return NumberBuffer;
});
