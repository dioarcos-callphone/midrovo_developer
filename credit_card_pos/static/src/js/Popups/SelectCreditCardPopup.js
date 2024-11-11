odoo.define('credit_card_pos.SelectCreditCardPopup', (require) => {
    const { _lt } = require('web.core');
    const { AbstractAwaitablePopup } = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class SelectCreditCardPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.selectedCard = null;
        }

        // Método para manejar la selección de la tarjeta
        selectCard(card) {
            this.selectedCard = card;
        }

        // Método para confirmar la selección
        confirm() {
            this.trigger('confirm', this.selectedCard);
            this.close();
        }

        // Método para cerrar el popup
        close() {
            this.trigger('close');
        }

        get cardList() {
            return this.props.list || [];
        }
    }

    SelectCreditCardPopup.template = 'credit_card_pos.SelectCreditCardPopup';

    SelectCreditCardPopup.defaultProps = {
        confirmText: _lt('Confirmar'),
        title: _lt('Seleccione la Tarjeta de Crédito'),
        body: _lt('Por favor, elija una tarjeta de crédito'),
        cancelKey: false,
    };

    // Registrar el componente en el Registries
    Registries.Component.add(SelectCreditCardPopup);

    return SelectCreditCardPopup;
});
