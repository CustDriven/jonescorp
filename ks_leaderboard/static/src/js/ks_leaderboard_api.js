odoo.define('ks_leaderboard.ks_leaderboard_api', function (require) {
    "use strict";

    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var core = require('web.core');
    var QWeb = core.qweb;

    return {

        render_lb_item_preview: function (ks_item_data, options) {
            options = options || {};

            var item_main_body_class = ["ks_lb_item_main_body", "grid-stack-item-content"];

            if (options.ks_is_preview) item_main_body_class.push("ks_lb_item_preview");

            if (options.ks_lb_manager) item_main_body_class.push("ks_lb_manager");
            else item_main_body_class.push("ks_lb_not_manager");

            item_main_body_class.push('item_header_' + ks_item_data.display.ks_header_layout_display);

            ks_item_data.ks_image_field ? item_main_body_class.push('ks_item_has_image') : item_main_body_class.push('ks_item_no_image') ;

            ks_item_data['ks_lb_list'] = options.ks_lb_list ? options.ks_lb_list: false;

            // Add theme top class here
            // .display.ks_item_theme_display
            // item_main_body_class.push("theme-v1-color");
            if (ks_item_data.display.ks_item_theme_gradient) {
                item_main_body_class.push('ks_item-' + ks_item_data.display.ks_item_theme_display + '-gradient');
            } else {
                item_main_body_class.push('ks_item-' + ks_item_data.display.ks_item_theme_display + '-color');
            }

            ks_item_data['item_main_body_class'] = item_main_body_class;

            var local_field_list = [].concat(ks_item_data.rank_field, ks_item_data.other_fields_list);


            // TODO : Later seperate this functoin
            // Monetary Field Handling. Later will handle for Integer and float formatting too.
            this._ks_format_item_number(ks_item_data);



            var $item_el = $(QWeb.render('ks_item_preview', ks_item_data));

            var item_cards_list = [].concat(ks_item_data.item_cards);
            
            // var $header_el = this['_ks_render_item_header_' + ks_item_data.display.ks_header_layout_display](ks_item_data, item_cards_list);
            var $header_el = $(QWeb.render('ks_leaderboard.item_header_'+ks_item_data.display.ks_header_layout_display, _.extend({item_card_list: item_cards_list},ks_item_data)));
            $item_el.find('.ks_lb_item_head_content').append($header_el);
            
            // var $body_el = this['_ks_render_item_body_' + ks_item_data.display.ks_body_layout_display](ks_item_data, item_cards_list);
            var $body_el = $(QWeb.render('ks_leaderboard.item_body_'+ ks_item_data.display.ks_body_layout_display, _.extend({item_card_list: item_cards_list},ks_item_data)));
            $item_el.find('.ks_lb_item_content').append($body_el);

            return $item_el
        },


        _ks_format_item_number: function(ks_item_data) {
            var self = this;
            var local_field_list = [].concat(ks_item_data.rank_field, ks_item_data.other_fields_list);
            var ks_currency = ks_item_data.ks_currency_id ? session.get_currency(ks_item_data.ks_currency_id) : false;

             _.each(ks_item_data.item_cards, function (card_data) {
                local_field_list.map(function (field) {
                    var actual_value = card_data[field]['value'];

                    if (card_data[field] && card_data[field]['type'] === "monetary") {
                        if (!actual_value) actual_value = 0.0;
                        var ks_num_formatted_value = self.ksNumFormatter(actual_value, 1);
                        var ks_formatted_value = field_utils.format.float(actual_value);

                        if (ks_currency && ks_currency.position === "after") {
                            ks_formatted_value += ' ' + ks_currency.symbol;
                            ks_num_formatted_value += ' ' + ks_currency.symbol;
                        } else if(ks_currency) {
                            ks_formatted_value = ks_currency.symbol + ' ' + ks_formatted_value;
                            ks_num_formatted_value = ks_currency.symbol + ' ' + ks_num_formatted_value;
                        }

                        card_data[field]['title_value'] = ks_formatted_value;
                        card_data[field]['show_value'] = ks_num_formatted_value;

                    }else if(card_data[field] && card_data[field]['type'] === "integer") {
                        if (!actual_value) actual_value = 0;
                        card_data[field]['show_value'] = self.ksNumFormatter(actual_value, 1);
                        card_data[field]['title_value'] = field_utils.format.integer(actual_value);

                    } else if (card_data[field] && card_data[field]['type'] === "float") {
                        if (!actual_value) actual_value = 0.0;
                        card_data[field]['show_value'] = self.ksNumFormatter(actual_value, 1);
                        card_data[field]['title_value'] = field_utils.format.float(actual_value);

                    }

                })

               if(ks_item_data.other_fields_list){
                    var name_initial = card_data[ks_item_data.other_fields_list[0]].value
                    if (typeof(name_initial)!=='string') name_initial = JSON.stringify(name_initial);
                    card_data['ks_pic_value'] = name_initial.split(" ").map((x) => x[0]).slice(0,2).join("");
                }

            })
        },


        _update_lb_item_data: function(ks_item_data) {
            var self = this;
            var item_cards_list = [].concat(ks_item_data.item_cards);

            self._ks_format_item_number(ks_item_data);

            var $header_el = $(QWeb.render('ks_leaderboard.item_header_'+ks_item_data.display.ks_header_layout_display, _.extend({item_card_list: item_cards_list},ks_item_data)));
            if (ks_item_data.$el.find('.ks_lb_item_head_content').children()[0]) {
                $(ks_item_data.$el.find('.ks_lb_item_head_content').children()[0]).replaceWith($header_el)
            } else {
                ks_item_data.$el.find('.ks_lb_item_head_content').append($header_el);
            }

            var $body_el = $(QWeb.render('ks_leaderboard.item_body_'+ ks_item_data.display.ks_body_layout_display, _.extend({item_card_list: item_cards_list},ks_item_data)));
            if (ks_item_data.$el.find('.ks_lb_item_content').children()[0]) {
                $(ks_item_data.$el.find('.ks_lb_item_content').children()[0]).replaceWith($body_el)
            } else {
                ks_item_data.$el.find('.ks_lb_item_content').append($body_el);
            }
        },

        _render_lb_item_search_box: function(ks_item_data, ks_search_input){
            var self = this;
            var ks_name = ks_item_data.other_fields_list[0];
            var item_cards_list = ks_item_data.item_cards.filter(function(card_data){
                return card_data[ks_name].value.toLocaleLowerCase().includes(ks_search_input.toLocaleLowerCase());
            })

            self._ks_format_item_number(ks_item_data);

            if(item_cards_list && item_cards_list.length>0) {
                var $search_box_el = $(QWeb.render('ks_leaderboard.item_body_'+ ks_item_data.display.ks_body_layout_display, _.extend({item_card_list: item_cards_list},ks_item_data)));
            }else {
                var $search_box_el = $(QWeb.render('ks_leaderboard.empty_item_search_box'));
            }

//            $search_box_el.prepend($(QWeb.render('ks_leaderboard.search_box_top_card')));

            ks_item_data.$el.find('.ks_remove_search_container').removeClass("ks_lb_hidden");

            if (ks_item_data.$el.find('.ks_lb_item_search_box').children()[0]) {
                $(ks_item_data.$el.find('.ks_lb_item_search_box').children()[0]).replaceWith($search_box_el)
            } else {
                ks_item_data.$el.find('.ks_lb_item_search_box').append($search_box_el);
            }

            ks_item_data.$el.find('.ks_lb_item_search_box').addClass('open');
        },


        ksNumFormatter: function (num, digits) {
            var negative;
            var si = [{
                    value: 1,
                    symbol: ""
                },
                {
                    value: 1E3,
                    symbol: "k"
                },
                {
                    value: 1E6,
                    symbol: "M"
                },
                {
                    value: 1E9,
                    symbol: "G"
                },
                {
                    value: 1E12,
                    symbol: "T"
                },
                {
                    value: 1E15,
                    symbol: "P"
                },
                {
                    value: 1E18,
                    symbol: "E"
                }
            ];
            if (num < 0) {
                num = Math.abs(num)
                negative = true
            }
            var rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
            var i;
            for (i = si.length - 1; i > 0; i--) {
                if (num >= si[i].value) {
                    break;
                }
            }
            if (negative) {
                return "-" + (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            } else {
                return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            }
        },


    }
})
