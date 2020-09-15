
odoo.define('wibtec.ribbon', function(require) {
"use strict";

    var rpc = require('web.rpc');
    var core = require('web.core');
    var HomeMenu = require('web_enterprise.HomeMenu');

    var QWeb = core.qweb;
    // Code from: http://jsfiddle.net/WK_of_Angmar/xgA5C/
    function validStrColour(strToTest) {
        if (strToTest === "") {
            return false;
        }
        if (strToTest === "inherit") {
            return true;
        }
        if (strToTest === "transparent") {
            return true;
        }
        var image = document.createElement("img");
        image.style.color = "rgb(0, 0, 0)";
        image.style.color = strToTest;
        if (image.style.color !== "rgb(0, 0, 0)") {
            return true;
        }
        image.style.color = "rgb(255, 255, 255)";
        image.style.color = strToTest;
        return image.style.color !== "rgb(255, 255, 255)";
    }

    HomeMenu.include({
        _render: function () {
            var self = this;
            rpc.query({
                model: 'wibtec.ribbon.backend',
                method: 'get_environment_ribbon',
            }).then(
                function (ribbon_data) {
                    if (ribbon_data.name && ribbon_data.name !== 'False') {
                        self.$el.find('.test-ribbon').html(QWeb.render('ribbon-db', { data: ribbon_data }));
                        self.$el.find('.test-ribbon').css('color', ribbon_data.color)
                        self.$el.find('.test-ribbon').css('background-color', ribbon_data.background_color)
                    }
                     // Ribbon color
                    if (ribbon_data.color && validStrColour(ribbon_data.color)) {
                        self.$el.find('.test-ribbon').css('color', ribbon_data.color)
                    }
                    // Ribbon background color
                    if (ribbon_data.background_color && validStrColour(ribbon_data.background_color)) {
                        self.$el.find('.test-ribbon').css('background-color', ribbon_data.background_color)
                    }
                }
            );
            return this._super.apply(this, arguments);
        },
    });
});
