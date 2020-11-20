odoo.define('website_custom_pages.formsv', function (require) {
'use strict';

var core = require('web.core');
var time = require('web.time');
var ajax = require('web.ajax');
var publicWidget = require('web.public.widget');
var session = require('web.session');
var rpc = require('web.rpc');
var _t = core._t;
var qweb = core.qweb;

$(document).ready(function(){
    $('.s_website_form').removeAttr("data-success_page")
    $("[name='email_from']").change(function(){
        var email = $("[name='email_from']").val();
        rpc.query({
            model: 'mail.suppression_list',
            method: 'check_email_domain',
            args: [email],
        })
        .then(function(res){
            if (res != ''){
                $("[name='email_from']").after('<div id="email_validation" style="color:red"></div>')
                $('#email_validation').append(res)
                $("[name='email_from']").val('');
            }else{
                $('#email_validation').css('display','none')
            }

        })
    }
    );
});

publicWidget.registry.form_builder_send.include({
    send: function (e) {
            e.preventDefault();  // Prevent the default submit behavior
            this.$target.find('.o_website_form_send').off().addClass('disabled');  // Prevent users from crazy clicking

            var self = this;

            self.$target.find('#o_website_form_result').empty();
            if (!self.check_error_fields({})) {
                self.update_status('invalid');
                return false;
            }

            // Prepare form inputs
            this.form_fields = this.$target.serializeArray();
            $.each(this.$target.find('input[type=file]'), function (outer_index, input) {
                $.each($(input).prop('files'), function (index, file) {
                    // Index field name as ajax won't accept arrays of files
                    // when aggregating multiple files into a single field value
                    self.form_fields.push({
                        name: input.name + '[' + outer_index + '][' + index + ']',
                        value: file
                    });
                });
            });

            // Serialize form inputs into a single object
            // Aggregate multiple values into arrays
            var form_values = {};
            _.each(this.form_fields, function (input) {
                if (input.name in form_values) {
                    // If a value already exists for this field,
                    // we are facing a x2many field, so we store
                    // the values in an array.
                    if (Array.isArray(form_values[input.name])) {
                        form_values[input.name].push(input.value);
                    } else {
                        form_values[input.name] = [form_values[input.name], input.value];
                    }
                } else {
                    if (input.value !== '') {
                        form_values[input.name] = input.value;
                    }
                }
            });

            // Post form and handle result
            ajax.post(this.$target.attr('action') + (this.$target.data('force_action')||this.$target.data('model_name')), form_values)
            .then(function (result_data) {
                result_data = JSON.parse(result_data);
                if (!result_data.id) {
                    // Failure, the server didn't return the created record ID
                    self.update_status('error');
                    if (result_data.error_fields) {
                        // If the server return a list of bad fields, show these fields for users
                        self.check_error_fields(result_data.error_fields);
                    }
                } else {
                    // Success, redirect or update status
                    var success_page = self.$target.attr('data-success_page');
                    if (success_page) {
                        $(window.location).attr('href', success_page);
                    }
                    else {
                        var typ_id = self.$target.find("[name='typ_id']").val();
                        var website_form = self.$target.find('.s_website_form')
                        self._rpc({
                                    route: '/thankyou',
                                    params: {
                                        typ_id: typ_id,
                                    },
                                }).then(function (data) {
                                    $('.s_website_form').after('<div id="thankmsg"></div>')
                                    $('#thankmsg').append(data)
                                    $('.s_website_form').css('display','none')
                                });
                         $('#thankyou').css('display','block')
                    }

                    // Reset the form
                    self.$target[0].reset();
                }
            })
            .guardedCatch(function (){
                self.update_status('error');
            });
        },


});

});