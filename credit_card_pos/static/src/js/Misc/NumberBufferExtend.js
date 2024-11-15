odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    // Sobrescribimos el método `deactivate`
    NumberBuffer.include({
        deactivate: function () {
            // Eliminar el listener del teclado si está presente
            if (this.listenerAttached) {
                useExternalListener(window, "keyup", this._onKeyboardInput.bind(this), true);
                this.listenerAttached = false;
            }
        }
    });

    return NumberBuffer;
});
