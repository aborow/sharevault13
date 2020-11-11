odoo.define('web_widget_open_tab.FieldOpenTab', function(require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var ListRenderer = require('web.ListRenderer');
    var core = require('web.core');
    var config = require('web.config');
    var qweb = core.qweb;
    var _t = core._t;

     $(document).ready(function() {
         console.log("ffffffffffffffffffffffffff",window.location.href, window.location.href.indexOf("/document/share"))
        if (window.location.href.indexOf("/document/share") > -1) {
            alert("your url contains the name franky");
        }
  });

    var FieldOpenTab = AbstractField.extend({
        description: "",
        supportedFieldTypes: ['integer'],
        events: _.extend({}, AbstractField.prototype.events, {
            'click': '_onClick',
        }),
        isSet: function () {
            return true;
        },
        _getReference: function () {
            var url = new URL(window.location.href);
            function replaceUrlParam(url, paramName, paramValue){
                    if(paramValue == null || paramValue == "")
                        return url
                        .replace(new RegExp('[?&]' + paramValue + '=[^&#]*(#.*)?$'), '$1')
                        .replace(new RegExp('([?&])' + paramValue + '=[^&]*&'), '$1');
                    url = url.replace(/\?$/,'');
                    var pattern = new RegExp('\\b('+paramName+'=).*?(&|$)')
                    if(url.search(pattern)>=0){
                        return url.replace(pattern,'$1' + paramValue + '$2');
                    }
                    return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue
                }
            return replaceUrlParam(window.location.href,'id', this.res_id)
        },
        _renderReadonly: function () {
            var $content = $(
                '<a href="'+ this._getReference() + '">'
            ).addClass('open_tab_widget fa fa-external-link');
            var self = this;
            $content.tooltip({
                delay: { show: 1000, hide: 0 },
                title: function () {
                    return qweb.render('WidgetButton.tooltip', {
                        debug: config.debug,
                        state: self.record,
                        node: {
                            attrs: {
                                'help': _t('Click in order to open on new tab'),
                                'type': _t('Widget')
                            }
                        },
                    });
                },
            });
            this.$el.append($content)
        },
        _onClick: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var element = $(ev.currentTarget).find('a');
            if (element != null && element[0].href != null) {
                window.open(this._getReference());
            }
        },
    });

    field_registry.add('open_tab', FieldOpenTab);
    return FieldOpenTab;

});
