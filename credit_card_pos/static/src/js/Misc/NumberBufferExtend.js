odoo.define("credit_card_pos.NumberBufferExtend", (require) => {
    "use strict";

    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const NumberBufferExtend = NumberBuffer.extend({
        init() {
            this._super(...arguments);
            this.keyboardEnabled = true; // Nueva propiedad para manejar el estado del teclado
        },

        /**
         * Deshabilita el manejo del teclado.
         */
        disableKeyboard() {
            this.keyboardEnabled = false;
        },

        /**
         * Habilita el manejo del teclado.
         */
        enableKeyboard() {
            this.keyboardEnabled = true;
        },

        /**
         * Sobrescribe el método _onKeyboardInput para verificar si el teclado está habilitado.
         */
        _onKeyboardInput(event) {
            if (!this.keyboardEnabled) {
                return; // Ignorar eventos del teclado si está deshabilitado
            }
            return this._super(event);
        },

        /**
         * Sobrescribe el método _onNonKeyboardInput para verificar si el teclado está habilitado.
         */
        _onNonKeyboardInput(event) {
            if (!this.keyboardEnabled) {
                return; // Ignorar eventos no provenientes del teclado si está deshabilitado
            }
            return this._super(event);
        },
    });

    // Sobrescribe el `NumberBuffer` global con la versión extendida
    return new NumberBufferExtend();
});
