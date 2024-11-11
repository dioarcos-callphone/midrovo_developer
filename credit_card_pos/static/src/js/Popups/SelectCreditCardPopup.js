odoo.define('credit_card_pos.SelectCreditCardPopup', function (require) {
    const { Component } = require('owl');
    const { useState } = require('owl.hooks');
    const { _t } = require('web.core');
    const Registries = require('point_of_sale.Registries');

    class SelectCreditCardPopup extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                selectedCard: null,
            });
        }

        // Método para manejar la selección de la tarjeta
        selectCard(card) {
            this.state.selectedCard = card;
        }

        // Cerrar el popup
        close() {
            this.trigger('close');
        }

        // Confirmar la selección
        confirm() {
            this.trigger('confirm', this.state.selectedCard);
        }

        get cardList() {
            return this.props.list || [];
        }
    }

    SelectCreditCardPopup.template = 'credit_card_pos.SelectCreditCardPopup';

    // Registrar el componente en el Registries
    Registries.Component.add(SelectCreditCardPopup);

    return SelectCreditCardPopup;
});
