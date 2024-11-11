odoo.define("credit_card_pos.PSNumpadInputButtonExtend", (require) => {
    "use strict";

    const Registries = require('point_of_sale.Registries');
    const PSNumpadInputButton = require('point_of_sale.PSNumpadInputButton');

    // Crear una clase heredada
    const PSNumpadInputButtonExtended = PSNumpadInputButton => class extends PSNumpadInputButton {
        setup() {
            super.setup()
            console.log('ENTRAMOS AL PS NUMPAD INPUT BUTTON')
        }
    }

    // Registrar el componente extendido en el registro de componentes
    Registries.Component.extend(PSNumpadInputButton, PSNumpadInputButtonExtended);

    // Exportar el componente extendido
    return PSNumpadInputButtonExtended;
})
