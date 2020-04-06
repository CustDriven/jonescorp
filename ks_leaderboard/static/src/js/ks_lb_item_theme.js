odoo.define('ks_leaderboard.ks_lb_item_theme', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');

    var QWeb = core.qweb;

    //Widget for lb item theme using while creating lb item.
    var KsLbTheme = AbstractField.extend({

        supportedFieldTypes: ['char'],

        events: _.extend({}, AbstractField.prototype.events, {
            'click .ks_lb_theme_input_container': 'ks_lb_theme_input_container_click',
        }),

        _render: function () {
            var self = this;
            self.$el.empty();
            var $view = $(QWeb.render('ks_lb_theme_view'));
            if (self.value) {
                $view.find("input[value='" + self.value + "']").prop("checked", true);
            }
            self.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.ks_lb_theme_view_render').addClass('ks_not_click');
            }
        },

        ks_lb_theme_input_container_click: function (e) {
            var self = this;
            var $box = $(e.currentTarget).find(':input');
            if ($box.is(":checked")) {
                self.$el.find('.ks_lb_theme_input').prop('checked', false)
                $box.prop("checked", true);
            } else {
                $box.prop("checked", true);
            }
            self._setValue($box[0].value);
        },
    });

    registry.add('ks_lb_item_theme', KsLbTheme);

    return {
        KsLbTheme: KsLbTheme
    };

});