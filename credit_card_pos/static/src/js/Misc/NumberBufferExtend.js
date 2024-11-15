odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    const Registries = require("point_of_sale.Registries");

    const { removeExternalListener } = owl;

    const NumberBufferExtend = (NumberBuffer) => class NumberBufferExtend extends NumberBuffer {
            deactivate() {
                // Eliminar el listener de 'keyup'
                removeExternalListener(window, "keyup", this._onKeyboardInput.bind(this));
            }

        };

    // Registramos la nueva clase heredada en los registros de Odoo
    Registries.Model.extend(NumberBuffer, NumberBufferExtend);

});