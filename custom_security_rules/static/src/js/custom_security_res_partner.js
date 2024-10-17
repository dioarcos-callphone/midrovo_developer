/** @odoo-module **/

import { Component } from 'owl';
import { useSession } from '@web/core/session';
import { registry } from '@web/core/registry';

class MyComponent extends Component {
    setup() {
        super.setup(...arguments);
        this.session = useSession();
        this.userHasEditAccess = this.hasEditPermissions();
    }

    hasEditPermissions() {
        // Verificar si el usuario pertenece al grupo
        return this.session.user_groups.includes('custom_security_rules.group_custom_security_role_user_2');
    }
}

registry.category('actions').add('my_component', MyComponent);
