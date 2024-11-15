odoo.define('credit_card_pos.NumberBufferExtend', function (require) {
    "use strict";

    // Importa el módulo o clase original que deseas extender
    const NumberBuffer = require('your_module_name.NumberBuffer');  // Asegúrate de que la ruta sea correcta

    // Extiende la clase NumberBuffer
    const NumberBufferExtend = NumberBuffer.extend({
        // Agrega métodos o propiedades adicionales si es necesario
        newMethod: function() {
            console.log('Método extendido');
            // Implementación adicional
        },

        // Sobrescribe un método existente si lo necesitas
        reset: function() {
            this._super();  // Llama al método original de la clase padre
            console.log('Buffer ha sido reseteado');
            // Puedes agregar lógica extra aquí
        }
    });

    // Retorna la clase extendida para que pueda ser utilizada por otros módulos de Odoo
    return NumberBufferExtend;
});
