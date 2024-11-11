odoo.define("credit_card_pos.PSNumpadInputButton", (require) => {
    const PosComponent = require("point_of_sale.PosComponent");
    const Registries = require("point_of_sale.Registries");
    
    // Asegúrate de que el modal esté registrado en el `Registries.Component`
    const CreditCardModal = require("credit_card_pos.CreditCardModal"); 

    class PSNumpadInputButton extends PosComponent {
        get _class() {
            return this.props.changeClassTo || "input-button number-char";
        }

        // Sobrescribir el método de clic
        onClick() {
            if (this.props.value === 'credit_card') {  // Verifica si el valor es "tarjeta de crédito"
                // Usar datos quemados
                const creditCards = [
                    { id: 1, name: "Visa" },
                    { id: 2, name: "MasterCard" },
                    { id: 3, name: "American Express" },
                ];

                // Abre el modal de selección de tarjetas de crédito
                this.showPopup('CreditCardModal', {  // Nombre del modal debe ser un string
                    title: "Selecciona una tarjeta de crédito",
                    creditCards: creditCards, // Pasar lista de tarjetas
                }).then((selectedCard) => {
                    if (selectedCard) {
                        // Procesa la tarjeta seleccionada y continúa el flujo
                        this.trigger('input-from-numpad', { key: selectedCard.name });
                    }
                });
            } else {
                // Si no es "tarjeta de crédito", continúa el flujo normal
                this.trigger('input-from-numpad', { key: this.props.value });
            }
        }
    }

    PSNumpadInputButton.template = "PSNumpadInputButton";
    Registries.Component.add(PSNumpadInputButton);
});
