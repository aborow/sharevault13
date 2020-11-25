odoo.define('sharevault_custom.menu', function (require) {
'use strict';

var dom = require('web.dom');
var publicWidget = require('web.public.widget');
var wUtils = require('website.utils');
publicWidget.registry.affixMenu = publicWidget.Widget.extend({
    selector: 'header.o_affix_enabled',

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);

        var self = this;
        this.$headerClone = this.$target.clone().addClass('o_header_affix affix').removeClass('o_affix_enabled').removeAttr('id');
        this.$headerClone.insertAfter(this.$target);
        this.$headers = this.$target.add(this.$headerClone);
        this.$dropdowns = this.$headers.find('.dropdown');
        this.$dropdownMenus = this.$headers.find('.dropdown-menu');
        this.$navbarCollapses = this.$headers.find('.navbar-collapse');

        this._adaptDefaultOffset();
        wUtils.onceAllImagesLoaded(this.$headerClone).then(function () {
            self._adaptDefaultOffset();
        });

        // Handle events for the collapse menus
        _.each(this.$headerClone.find('[data-toggle="collapse"]'), function (el) {
            var $source = $(el);
            var targetIDSelector = $source.attr('data-target');
            var $target = self.$headerClone.find(targetIDSelector);
            $source.attr('data-target', targetIDSelector + '_clone');
            $target.attr('id', targetIDSelector.substr(1) + '_clone');
        });
        // While scrolling through navbar menus, body should not be scrolled with it
        this.$headerClone.find('div.navbar-collapse').on('show.bs.collapse', function () {
            $(document.body).addClass('overflow-hidden');
        }).on('hide.bs.collapse', function () {
            $(document.body).removeClass('overflow-hidden');
        });

        // Window Handlers
        $(window).on('resize.affixMenu scroll.affixMenu', _.throttle(this._onWindowUpdate.bind(this), 200));
        setTimeout(this._onWindowUpdate.bind(this), 0); // setTimeout to allow override with advanced stuff... see themes

        return def.then(function () {
            self.trigger_up('widgets_start_request', {
                $target: self.$headerClone,
            });
        });
    },
    /**
     * @override
     */
    destroy: function () {
        if (this.$headerClone) {
            this.$headerClone.remove();
            $(window).off('.affixMenu');
        }
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _adaptDefaultOffset: function () {
        var bottom = this.$target.offset().top + this._getHeaderHeight();
        this.$headerClone.css('margin-top', Math.min(-200, -bottom) + 'px');
    },
    /**
     * @private
     */
    _getHeaderHeight: function () {
        return this.$headerClone.outerHeight();
    },

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
        this.$headerClone.toggleClass('affixed', wOffset > (hOffset - 50));
        // Reset opened menus
        this.$dropdowns.add(this.$dropdownMenus).removeClass('show');
        this.$navbarCollapses.removeClass('show').attr('aria-expanded', false);
    },
});
});
