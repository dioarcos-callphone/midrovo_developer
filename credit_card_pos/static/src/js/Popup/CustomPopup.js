odoo.define("credit_card_pos.CustomSelectionPopup", (require) => {
    "use strict";

    // Importamos las dependencias necesarias
    const SelectionPopup = require("@point_of_sale/js/Popups/SelectionPopup");
    const { useListener } = require("web.custom_hooks");
    const { removeEventListener, addEventListener } = owl;

    // Extiende la clase SelectionPopup
    const CustomSelectionPopup = (SelectionPopup) =>
        class extends SelectionPopup {
            constructor() {
                super(...arguments); // Llamamos al constructor de la clase base
                useListener("show-popup", this._onPopupShown);  // Escuchamos cuando el popup se muestra
                useListener("close-popup", this._onPopupClosed); // Escuchamos cuando el popup se cierra
            }

            setup() {
                super.setup(); // Llamamos a la configuración original de SelectionPopup
                // Agregamos nuestra lógica de setup personalizada si es necesario
            }

            _onPopupShown() {
                console.log("Popup mostrado: desactivando teclado");
                // Aquí desactivamos el NumberBuffer para el evento de teclado
                NumberBuffer.deactivate();
            }

            _onPopupClosed() {
                console.log("Popup cerrado: reactivando teclado");
                // Reactivamos el NumberBuffer cuando se cierra el popup
                NumberBuffer.activate();
            }
        };

    // Registramos el componente extendido
    Registries.Component.add(CustomSelectionPopup);

    return CustomSelectionPopup;
});
