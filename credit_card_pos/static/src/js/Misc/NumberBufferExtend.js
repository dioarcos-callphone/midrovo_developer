odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";
    
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const Registries = require("point_of_sale.Registries");
    // const { removeExternalListener } = owl;

    // Extiende la clase NumberBuffer
    const NumberBufferExtend = NumberBuffer =>
        class extends NumberBuffer {
            // deactivate() {
            //     // Eliminar el listener de 'keyup'
            //     removeExternalListener(window, "keyup", this._onKeyboardInput.bind(this));
            // }
        };

    // Registramos la clase extendida en el sistema de registros de Odoo
    Registries.Component.extend(NumberBuffer, NumberBufferExtend);
});
