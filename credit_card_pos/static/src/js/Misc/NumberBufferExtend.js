odoo.define('credit_card_pos.NumberBufferExtend', function (require) {
    "use strict";

    const NumberBuffer = require('point_of_sale.NumberBuffer');  // Ruta correcta para importar NumberBuffer

    // Agrega métodos o propiedades adicionales a esta clase
    NumberBuffer.newMethod = function () {
        console.log('Método extendido');
        // Implementación adicional
    };

    return new NumberBuffer();
});
