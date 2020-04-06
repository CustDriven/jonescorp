odoo.define('ks_leaderboard.ks_leaderboard_controller', function (require) {
    "use strict";


    var AbstractController = require('web.AbstractController');
    var config = require('web.config');

    var BasicController = require('web.BasicController');

    var LeaderboardController = AbstractController.extend({
        custom_events: _.extend({}, AbstractController.prototype.custom_events, {
            ks_reload_view: '_onKsReloadview',
            ks_update_name: function (options) {
                this.displayName = options.data.ks_name ? options.data.ks_name : this.displayName;
            },
            ks_add_item: '_onKsAddItem',
            ks_update_item: '_ksUpdateItem',
            ks_copy_item: '_ksCopyItem',
            open_record: '_onKsOpenRecord',
        }),

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.ks_leaderboard_id = params.initialState.res_id;
            this._title = params.initialState.data.name;
            self.ks_reload_params = false;

        },


        _onKsReloadview: function (options) {
            var self = this;
            self.ks_reload_params = {
                ks_reload_status: 'ks_update_all_item',
                ks_lb_id: self.ks_leaderboard_id,
            };
            self.reload();
        },


        _ksUpdateItem: function (options) {
            options = options || {};
            if (options.data.id && options.data.value) {
                options['def'] = this._rpc({
                    model: 'ks_leaderboard.leaderboard.item',
                    method: 'write',
                    args: [options.data.id, options.data.value],
                })
            }
        },

        _ksCopyItem: function (options) {
            options = options || {};
            if (options.data.id && options.data.value) {
                options['def'] = this._rpc({
                    model: 'ks_leaderboard.leaderboard.item',
                    method: 'copy',
                    args: [options.data.id, options.data.value],
                }).then(function (result) {
                    return result;
                });
            }
        },

        _onKsAddItem: function (ev) {
            var self = this;

            self.ks_reload_params = {
                ks_reload_status: 'ks_update_all_item',
                ks_lb_id: self.ks_leaderboard_id,
            };
            
            var action_info = {
                type: 'ir.actions.act_window',
                res_model: 'ks_leaderboard.leaderboard.item',
                view_id: 'ks_leaderboard.leaderboard_item_form',
                views: [
                    [false, 'form']
                ],
                target: 'current',
                context: {
                    'form_view_initial_mode': 'edit',
                    'default_ks_leaderboard_id': this.ks_leaderboard_id,
                },
            };

            this.do_action(action_info

                );
        },

        _onKsOpenRecord: function (options) {
            var self = this;
            options = options || {};

            self.ks_reload_params = {
                ks_reload_status: 'ks_update_all_item',
                ks_lb_id: self.ks_leaderboard_id,
            };

            if (options.data.id) {
                var action_info = {
                    type: 'ir.actions.act_window',
                    res_model: 'ks_leaderboard.leaderboard.item',
                    res_id: options.data.id,
                    view_id: 'ks_leaderboard.leaderboard_item_form',
                    views: [
                        [false, 'form']
                    ],
                    target: 'current',
                    context: {
                        'form_view_initial_mode': 'edit',
                        'default_ks_leaderboard_id': this.ks_leaderboard_id,
                    },
                };

                this.do_action(action_info, {

                });
            }

        },

        ks_on_reverse_breadcrumb: function (ev) {
            // this.model.load(this);
            this.ks_reload_status = "ks_update";

        },

        ks_on_close: function (ev) {
            this.ks_reload_status = "ks_update";
            this.reload();

        },

        /**
         * 
         * @param {Object} params : 
         * @param.ks_reload_status : ks_update_single_item || ks_update_all_item
         * @param
         */
        reload: function (params) {
            var self = this;
            if (self.ks_reload_params) {
                var reload_params = self.ks_reload_params;
                self.ks_reload_params = false;
                return this.update(reload_params , {reload: true});
            } else {
                return this._super.apply(this,arguments);
            }

        },

    });

    return LeaderboardController;

});