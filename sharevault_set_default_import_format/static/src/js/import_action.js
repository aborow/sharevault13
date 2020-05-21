odoo.define('sharevault_set_default_import_format.import_sharevault', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var time = require('web.time');
var AbstractWebClient = require('web.AbstractWebClient');
var Loading = require('web.Loading');

var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var StateMachine = window.StateMachine;

var DataImport_sharevault = require('base_import.import');

function jsonp(form, attributes, callback) {
    attributes = attributes || {};
    var options = {jsonp: _.uniqueId('import_callback_')};
    window[options.jsonp] = function () {
        delete window[options.jsonp];
        callback.apply(null, arguments);
    };
    if ('data' in attributes) {
        _.extend(attributes.data, options);
    } else {
        _.extend(attributes, {data: options});
    }
    _.extend(attributes, {
        dataType: 'script',
    });
    $(form).ajaxSubmit(attributes);
}
function _make_option(term) { return {id: term, text: term }; }
function _from_data(data, term) {
    return _.findWhere(data, {id: term}) || _make_option(term);
}

/**
 * query returns a list of suggestion select2 objects, this function:
 *
 * * returns data exactly matching query by either id or text if those exist
 * * otherwise it returns a select2 option matching the term and any data
 *   option whose id or text matches (by substring)
 */
function dataFilteredQuery(q) {
    var suggestions = _.clone(this.data);
    if (q.term) {
        var exact = _.filter(suggestions, function (s) {
            return s.id === q.term || s.text === q.term;
        });
        if (exact.length) {
            suggestions = exact;
        } else {
            suggestions = [_make_option(q.term)].concat(_.filter(suggestions, function (s) {
                return s.id.indexOf(q.term) !== -1 || s.text.indexOf(q.term) !== -1
            }));
        }
    }
    q.callback({results: suggestions});
}


DataImport_sharevault.DataImport.include({
    start: function () {
        var self = this;
        this.$form = this.$('form');
        this.setup_encoding_picker();
        this.setup_separator_picker();
        this.setup_float_format_picker();
        this.setup_date_format_picker();

        return Promise.all([
            this._super(),
            self.create_model().then(function (id) {
                self.id = id;
                self.$('input[name=import_id]').val(id);

                self.renderButtons();
                var status = {
                    cp_content: {$buttons: self.$buttons},
                };
                self.updateControlPanel(status);
            }),
        ]);
    },

    setup_encoding_picker: function () {
        var data_option = this.$('input.oe_import_encoding').select2({
            width: '50%',
            data: _.map(('utf-8 utf-16 windows-1252 latin1 latin2 big5 gb18030 shift_jis windows-1251 koir8_r').split(/\s+/), _make_option),
            query: dataFilteredQuery,
            initSelection: function ($e, c) {
                if ($e && $e[0].value && $e[0].value != 'utf-8'){
                    $e[0].value = 'utf-8'
                }       
                return c(_make_option($e.val()));
            }
        });
    },
});


});
