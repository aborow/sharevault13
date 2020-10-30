odoo.define('website_custom_pages.form', function (require) {
'use strict';

var core = require('web.core');
var FormEditorRegistry = require('website_form.form_editor_registry');
var Dialog = require('web.Dialog');
var qweb = core.qweb;
var _t = core._t;
var rpc = require('web.rpc');
var WCPFormEditorDialog = require('website_form_editor');
var options = require('web_editor.snippets.options');
var wUtils = require('website.utils');
var Wysiwyg = require('web_editor.wysiwyg');
var Website_form = require('website_form.animation');
var time = require('web.time');
var ajax = require('web.ajax');
var publicWidget = require('web.public.widget');

var FormEditorDialog = Dialog.extend({
        /**
         * @constructor
         */
        init: function (parent, options) {
            this._super(parent, _.extend({

                buttons: [{
                    text: _t('Save'),
                    classes: 'btn-primary',
                    close: true,
                    click: this._onSaveModal.bind(this),
                }, {
                    text: _t('Cancel'),
                    close: true
                }],
            }, options));
        },

        //----------------------------------------------------------------------
        // Handlers
        //----------------------------------------------------------------------

        /**
         * @private
         */
        _onSaveModal: function () {
            if (this.$el[0].checkValidity()) {
                this.trigger_up('save');
            } else {
                _.each(this.$el.find('.o_website_form_input'), function (input) {
                    var $field = $(input).closest('.form-field');
                    $field.removeClass('o_has_error').find('.form-control, .custom-select').removeClass('is-invalid');
                    if (!input.checkValidity()) {
                        $field.addClass('o_has_error').find('.form-control, .custom-select').addClass('is-invalid');
                    }
                });
            }
        },
    });


 options.registry.website_form_editor.include({

       website_form_model_modal: function (previewMode, value, $li) {
            var self = this;
            this._rpc({
                model: "ir.model",
                method: "search_read",
                args: [
                    [['website_form_access', '=', true], ['website_form_key', '!=', false]],
                    ['id', 'model', 'name', 'website_form_label', 'website_form_key']
                ],
            }).then(function (models) {
                self.models = models;
                // Models selection input
                var modelSelection = qweb.render("website_form.field_many2one", {
                    field: {
                        name: 'model_selection',
                        string: 'Action',
                        required: true,
                        records: _.map(models, function (m) {
                            return {
                                id: m.id,
                                display_name: m.website_form_label || m.name,
                                selected: (m.model === self.$target.attr('data-model_name')) ? 1 : null,
                            };
                        }),
                    }
                });

                // Success page input
                var successPage = qweb.render("website_form.field_char", {
                    field: {
                        name: 'success_page',
                        string: 'Thank You Page',
                        value: self.$target.attr('data-success_page')
                    }
                });

                var save = function () {
                    var successPage = this.$el.find("[name='success_page']").val();
                    self.init_form();
                    self.$target.attr('data-success_page', successPage);
    //                    self.$target.removeAttr("data-success_page")
//                    this.$el.find('.s_website_form').removeClass('container-fluid mt32');
                    this.$el.find('.o_form_parameter_custom').each(function () {
                        var $field = $(this).find('.o_website_form_input');
                        var value = $field.val();
                        var fieldName = $field.attr('name');
                        self.$target.find('.form-group:has("[name=' + fieldName + ']")').remove();
                        if (value) {
                            var $hiddenField = $(qweb.render('website_form.field_char', {
                                field: {
                                    name: fieldName,
                                    value: value,
                                }
                            })).addClass('d-none');
                            self.$target.find('.form-group:has(".o_website_form_send")').before($hiddenField);
                        }
                    });
               };

                var cancel = function () {
                    if (!self.$target.attr('data-model_name')) {
                        self.$target.remove();
                    }
                };

                var $content = $('<form role="form">' + modelSelection + successPage + '</form>');
                    var dialog = new FormEditorDialog(self, {
                    title: 'Form Parameters',
                    size: 'medium',
                    $content: $content,
                }).open();
                dialog.on('closed', this, cancel);
                dialog.on('save', this, ev => {
                    ev.stopPropagation();
                    save.call(dialog);
                });

                wUtils.autocompleteWithPages(self, $content.find("input[name='success_page']"));
                self.originSuccessPage = $content.find("input[name='success_page']").val();
                self.originFormID = $content.find("[name='model_selection']").val();
                self._renderParameterFields($content);
                $content.find("[for='success_page']").css('display','none')
                $content.find("[name='success_page']").css('display','none')
//                $content.find("[name='model_selection']").attr('disabled',true)
                $content.find("[name='model_selection']").on('change', function () {
                    self._renderParameterFields($content);
                });
            });
        },
})

$(document).ready(function(){
    $('.s_website_form').removeAttr("data-success_page")
});



FormEditorRegistry.add('create_svlead', {
    defaultTemplateName: 'website_custom_pages.default_sv_form',
    defaultTemplatePath: '/website_custom_pages/static/src/xml/website_sv_form.xml',
    fields: [
    {
        name: 'typ_id',
        type: 'many2one',
        relation: 'web.thankyou.pages',
        string: _t('Thank You Messages'),
        title: _t('Select Respective Thank You Message'),
    },
    {
        name: 'source_id',
        type: 'many2one',
        relation: 'utm.source',
        string: _t('Source'),
        title: _t('Select Source of Form'),

    },
    {
        name: 'share_link_id',
        type: 'many2one',
        relation: 'documents.share',
        string: _t('Share Link'),
        title: _t('Select Document Share Link'),

    },
    {
        name: 'team_id',
        type: 'many2one',
        relation: 'crm.team',
        domain: [['use_opportunities', '=', true]],
        string: _t('Sales Channel'),
        title: _t('Assign leads/opportunities to a sales channel.'),
    },
    {
        name: 'user_id',
        type: 'many2one',
        relation: 'res.users',
        string: _t('Salesperson'),
        title: _t('Assign leads/opportunities to a salesperson.'),
    },
    {
        name: 'campaign_id',
        type: 'many2one',
        relation: 'utm.campaign',
        string: _t('Campaign'),
        title: _t('Select related Campaign'),
    }],
});

});