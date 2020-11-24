odoo.define('website.content.menu', function (require) {
'use strict';

var dom = require('web.dom');
var publicWidget = require('web.public.widget');
var wUtils = require('website.utils');

publicWidget.registry.affixMenu = publicWidget.Widget.extend({
    selector: 'header.o_affix_enabled',

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Called when the window is resized or scrolled -> updates affix status and
     * automatically closes submenus.
     *
     * @private
     */
    _onWindowUpdate: function () {
        if (this.$navbarCollapses.hasClass('show')) {
            return;
        }

        var wOffset = $(window).scrollTop();
        var hOffset = this.$target.scrollTop();

        // THIS IS HOW IT WAS
        //this.$headerClone.toggleClass('affixed', wOffset > (hOffset + 300));

        // THIS IS HOW IT SHOULD BE
        this.$headerClone.toggleClass('affixed', wOffset > (hOffset + -50));

        // Reset opened menus
        this.$dropdowns.add(this.$dropdownMenus).removeClass('show');
        this.$navbarCollapses.removeClass('show').attr('aria-expanded', false);
    },
});
