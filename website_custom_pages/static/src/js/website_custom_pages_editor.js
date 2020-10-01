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
                var typ = document.getElementById('thankyou_pages');
                var source = document.getElementById('sources');
                var user_id = document.getElementById('user_id');
                var share_link_id = document.getElementById('share_link_id');
                console.log('\n typ',typ)
                console.log('\n source',source)
                console.log('\n user_id',user_id)
                console.log('\n share_link_id',share_link_id)
                typ.value = this.$el.find("[name='typ_id']").val();
                source.value = this.$el.find("[name='source']").val();
                user_id.value = this.$el.find("[name='user_id']").val();
                share_link_id.value = this.$el.find("[name='share_link_id']").val();
                var tp = this.$el.find("[name='typ_id']").val();
                console.log('\n typ v',tp)
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
//                    var source = document.getElementById('sources');
//                    var typ = document.getElementById('thankyou_pages');
//                    var user_id = document.getElementById('user_id');
//                    var share_link_id = document.getElementById('share_link_id');
//                    typ.value = ev.target.$el.find("[name='typ_id']").val();
//                    source.value = ev.target.$el.find("[name='source']").val();
//                    user_id.value = ev.target.$el.find("[name='user_id']").val();
//                    share_link_id.value = ev.target.$el.find("[name='share_link_id']").val();
                    ev.stopPropagation();
                    save.call(dialog);
                });

                wUtils.autocompleteWithPages(self, $content.find("input[name='success_page']"));
                self.originSuccessPage = $content.find("input[name='success_page']").val();
                self.originFormID = $content.find("[name='model_selection']").val();
                self._renderParameterFields($content);
                $content.find("[for='success_page']").css('display','none')
                $content.find("[name='success_page']").css('display','none')
                $content.find("[name='model_selection']").attr('disabled',true)
                $content.find("[name='model_selection']").on('change', function () {
                    self._renderParameterFields($content);
                });
            });
        },
})


$(document).ready(function(){

    $('.s_website_form').removeAttr("data-success_page")
    $('.o_website_form_send').click(function(e){
        var thankyou_id = $(this).parent().find('#thankyou_pages').val()
        var website_form = $(this).parents('.s_website_form')
        $(website_form).css('display','none')
        $('.form-wtr').css('display','none')
        rpc.query({
                    model: 'web.thankyou.pages',
                    method: 'search_read',
                    domain: [['id', 'in', [thankyou_id]]],
                    fields: ['text'],
                }).then(function (result) {
                    $('#thankyou').append(result[0].text)
                })

         $('#thankyou').css('display','block')

    })

});

FormEditorRegistry.map.create_lead.fields.shift();


FormEditorRegistry.map.create_lead.fields.push(
    {
        name: 'typ_id',
        type: 'many2one',
        relation: 'web.thankyou.pages',
        string: _t('Thank You Messages'),
        title: _t('Select Respective Thank You Message'),
    },
    {
        name: 'source',
        type: 'char',
        relation: 'crm.lead',
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

);
});