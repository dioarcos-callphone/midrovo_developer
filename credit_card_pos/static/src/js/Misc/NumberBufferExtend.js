odoo.define('credit_card_pos.NumberBufferExtend', function (require) {
    "use strict";

    // Importa el módulo o clase original que deseas extender
    const NumberBuffer = require('point_of_sale.NumberBuffer');  // Ruta correcta para importar NumberBuffer

    // Crea una nueva clase que contenga una instancia de NumberBuffer
    const NumberBufferExtend = function () {
        this.numberBufferInstance = new NumberBuffer();
    };

    // Agrega métodos o propiedades adicionales a esta clase
    NumberBufferExtend.prototype.newMethod = function () {
        console.log('Método extendido');
        // Implementación adicional
    };

    // Sobrescribe un método existente si lo necesitas
    NumberBufferExtend.prototype.reset = function () {
        this.numberBufferInstance.reset();  // Llama al método original de NumberBuffer
        console.log('Buffer ha sido reseteado');
        // Puedes agregar lógica extra aquí
    };

    return NumberBufferExtend;
});
