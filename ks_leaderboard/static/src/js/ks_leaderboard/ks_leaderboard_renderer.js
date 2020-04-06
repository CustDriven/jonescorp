odoo.define('ks_leaderboard.ks_leaderboard_renderer', function (require) {
    "use strict";


    var AbstractRenderer = require('web.AbstractRenderer');
    var core = require('web.core');
    var Dialog = require('web.Dialog');


    var KsLbApi = require('ks_leaderboard.ks_leaderboard_api');

    var qweb = core.qweb;
    var _t = core._t;

    var LeaderboardRenderer = AbstractRenderer.extend({

        // className: "o_ks_leaderboard_view",

        template: 'ks_leaderboard_view_template',

        events: {
            'click #ks_add_item': '_onKsAddItemClicked',
            'click #ks_lb_layout_edit': '_ksRenderEditMode',
            'click #ks_lb_save_layout': '_ksSaveLayout',
            'click #ks_lb_cancel_layout': '_ksCancelLayout',
            'click .ks_open_item': '_onKsOpenItemClicked',
            'click .ks_remove_item': '_onKsRemoveItem',
            'click .ks_move_item': '_onKsMoveItemClicked',
            'click .ks_duplicate_item': '_onKsDuplicateItemClicked',

            'focusin .ks_item_search_card_input': function(ev){
                var self = this;
                var item_el = self.ks_item_data[$(ev.currentTarget).data('id')].$el;
                item_el.find(".ks_lb_item_configs").removeClass("ks_lb_slide_up");
            },
            'focusout .ks_item_search_card_input': function(ev){
                if(ev.target.value === "") {
                    var self = this;
                    var item_el = self.ks_item_data[$(ev.currentTarget).data('id')].$el;
                    self.KsRemoveSearchContainer(item_el);
                    item_el.find(".ks_lb_item_configs").addClass("ks_lb_slide_up");
                }
            },

            'keyup .ks_item_search_card_input': '_onKsItemSearchInput',

            'click .ks_search_card_button': function(ev){
                var self = this;
                var ks_item = self.ks_item_data[$(ev.currentTarget).data('id')];
                var ks_search_value = ks_item.$el.find(".ks_item_search_card_input").val();
                self.KsItemSearchCards(ks_item, ks_search_value);
            },

            'click .ks_remove_search_container': '_onKsRemoveSearchContainer',



            // Gridstack Evenets
            'enable .grid-stack': '_onKsGridstackEnable',
            'disable .grid-stack': '_onKsGridstackDisable',
            'removed .grid-stack': '_onKsGridstackRemoved',

            'click .ks_bs_dropdown': function (e) {
                if (e.target.tagName!=="BUTTON") e.stopPropagation();
            },
        },

        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            this.$ks_header;
            this.$ks_toolbar;
            this.$ks_items;
            this.ks_leaderboard_data = state['data'] || {};

            //            To handle leaderboard delete case from another tab
            if (!state['data']) this.do_action('reload');

            this.ks_item_ids = this.ks_leaderboard_data['ks_leaderboard_item_ids'] || [];
            this.ks_item_data = state['item_data'] || {};
            this.ks_lb_list = state['ks_lb_list'] || [];
            this.ks_lb_manager = state.ks_lb_manager || false;
            this.ksItemRefreshIntervals = {};
            this.ks_state = {
                ks_edit_mode: false,
                ks_gs_item_update_list: [],
            };

            this.ks_gridstack_state = {
                'active': false,
            }

            this.ks_gridstack_config = {

                // Custom Grid length for gridstack. To use this, use extra CSS in view file.
                //width: 4,

                // resizable/draggable handle
                resizable: {
                    handles: 'se, sw'
                },

                //handles are shown even if the user is not hovering over the widget
                alwaysShowResizeHandle: false,

                // Animation on/off
                animate: true,

                // enable floating widgets
                //            float: true,

                // disables the onColumnMode when the window width is less than minWidth
                //    disableOneColumnMode: true,

                // turns grid to RTL
                //            rtl: true,

                // makes grid static

                float: false,
                itemClass: 'ks_grid-stack-item',
            }
        },

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        updateState: function (state, params) {
            this.state = state;
            if (params.ks_reload_status) {
                this[params.ks_reload_status]();
                return $.when();
            }

            return params.noRender ? $.when() : this._render();

        },

        ks_update_all_item: function () {
            var self = this;
            this.ks_leaderboard_data = this.state['data'] || {};
            this.ks_item_ids = this.state['data']['ks_leaderboard_item_ids'] || [];
            this.ks_item_data = this.state['item_data'] || {};
            this.ks_lb_list = this.state['ks_lb_list'] || [];

            this.$ks_lb_main_content.empty();
            this.ksRenderMainContentView(this.$ks_lb_main_content);

        },


        on_attach_callback: function () {
            var self = this;
            self.ksSetRefreshInterval();
        },

        on_detach_callback: function () {
            var self = this;
            if (self.grid) {
                self.grid.destroy();
            }

            self.ksRemoveRefreshInterval();

        },

        ksSetRefreshInterval: function () {
            var self = this;
            if (self.ks_item_ids.length > 0) {
                _.each(self.ks_item_ids, function (item_id) {
                    var updateValue = parseInt(self.ks_item_data[item_id].ks_refresh_rate);
                    if (updateValue) {
                        var ksItemUpdateInterval = setInterval(function () {
                            self.ksFetchUpdateItem(item_id)
                        }, updateValue*60000);
                        self.ksItemRefreshIntervals[item_id] = ksItemUpdateInterval;
                    }
                });
            }
        },

        ksFetchUpdateItem: function(ks_item_id){
            var self = this;

                return self._rpc({
                    route: '/ks_leaderboard/ks_lb_fetch_items_data',
                    params: {
                        ks_items_ids: [ks_item_id]|| [],
                    },
                }).then(function(updated_data) {
                    Object.assign(self.ks_item_data[ks_item_id],updated_data[ks_item_id])
                    self.ksReloadLeaderboardItemView([ks_item_id]);
                })
        },

        ksFetchAddItem: function(ks_item_id){
            var self = this;

                return self._rpc({
                    route: '/ks_leaderboard/ks_lb_fetch_items_data',
                    params: {
                        ks_items_ids: [ks_item_id]|| [],
                    },
                }).then(function(updated_data) {
                    Object.assign(self.ks_item_data,updated_data)
                    self.ksRenderLeaderBoardItems(self.grid, [ks_item_id], self.ks_item_data, self.ks_lb_list, self.ks_lb_manager)
                    self.ks_item_ids.push(ks_item_id)
                })
        },

        ksReloadLeaderboardItemView: function(ks_item_ids){
            var self = this;
            _.each(ks_item_ids, function (item_id) {
                KsLbApi._update_lb_item_data(self.ks_item_data[item_id])
            });

        },

        ksRemoveRefreshInterval: function () {
            var self = this;
            Object.values(self.ksItemRefreshIntervals).forEach(function(itemInterval){
                clearInterval(itemInterval);
            });
        },


        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        _render: function () {
            this.$ks_header = this.$el.find('div.ks_lb_header_container');
            this.ksRenderHeader();

            this.$ks_lb_main_content = this.$el.find('div.ks_lb_main_content');
            this.ksRenderMainContentView(this.$ks_lb_main_content);
            return $.when();
        },

        ksRenderHeader: function () {
            var $header = $(qweb.render("ks_lb_header_view", {
                ks_lb_name: this.ks_leaderboard_data.name,
                ks_lb_manager: this.ks_lb_manager,
                ks_edit_mode: this.ks_state['ks_edit_mode'],
            }));

            if (this.$ks_header.children()[0]) {
                $(this.$ks_header.children()[0]).replaceWith($header)
            } else {
                this.$ks_header.append($header);
            }
        },

        ksRenderMainContentView: function ($node) {
            if (this.ks_item_ids.length > 0) {
                var $main_item_view = $(qweb.render("ks_lb_item_content_view", {
                    data: this.ks_leaderboard_data
                }))
                $node.append($main_item_view);

                $node.find('.grid-stack').gridstack(this.ks_gridstack_config);
                this.grid = $node.find('.grid-stack').data('gridstack');

                this.ksRenderLeaderBoardItems(this.grid, this.ks_item_ids, this.ks_item_data, this.ks_lb_list, this.ks_lb_manager);

                // Make this so that it only saves the itemdata with no gridstack config
                this._ksSaveItemGridConfig(this.ks_item_data, this.ks_state.ks_gs_item_update_list);
                this.ks_state.ks_gs_item_update_list = [];

            } else {
                $node.append($(qweb.render("ks_lb_no_view_help")));
            }
        },

        ksRenderLeaderBoardItems: function (grid, ks_item_ids, ks_item_data, ks_lb_list, ks_lb_manager) {
            var self = this;
            _.each(ks_item_ids, function (item_id) {
                var item = ks_item_data[item_id];
                item['$el'] = KsLbApi.render_lb_item_preview(item, {
                    ks_is_preview: false,
                    ks_lb_list: ks_lb_list,
                    ks_lb_manager: ks_lb_manager,
                })
                // addWidget(el[, x, y, width, height, autoPosition, minWidth, maxWidth, minHeight, maxHeight, id])
                if (item.ks_gridstack_config) {
                    var grid_config = JSON.parse(item.ks_gridstack_config);
                    grid.addWidget(item['$el'], grid_config['x'], grid_config['y'], grid_config['width'], grid_config['height'], false, 3, null, 6, null, item_id);

                } else {
                    grid.addWidget(item['$el'], null, null, 3, 4, true, 3, null, 6, null, item_id);
                    self.ks_state.ks_gs_item_update_list.push(item_id);
                }
            });

            grid.disable();
        },

        _ksSaveItemGridConfig: function (ks_item_data, item_ids) {
            var self = this;
            _.each(item_ids, function (item_id) {
                var item_data = ks_item_data[item_id];
                var grid_config = item_data.$el.data('_gridstack_node');

                item_data.ks_gridstack_config = JSON.stringify({
                    x: grid_config.x,
                    y: grid_config.y,
                    width: grid_config.width,
                    height: grid_config.height,
                });

                self.trigger_up('ks_update_item', {
                    id: parseInt(grid_config.id),
                    value: {
                        ks_gridstack_config: item_data.ks_gridstack_config
                    }
                });
            });
        },


        // TODO :  this function event should be called directly from controller
        _onKsAddItemClicked: function (ev) {
            this.trigger_up('ks_add_item', {});
        },

        _onKsOpenItemClicked: function (ev) {
            if ($(ev.currentTarget).data('id')) {
                this.trigger_up('open_record', {
                    id: $(ev.currentTarget).data('id')
                });
            }
        },

        _onKsMoveItemClicked: function (ev) {
            var self = this;
            var $el = this.ks_item_data[$(ev.currentTarget).data('id')].$el;
            var lb_name = $el.find('.ks_lb_select option:selected').text();
            if ($el && parseInt($el.find('.ks_lb_select').val()) !== self.ks_leaderboard_data.id) {
                var result = self.trigger_up('ks_update_item', {
                    id: parseInt($(ev.currentTarget).data('id')),
                    value: {
                        ks_leaderboard_id: parseInt($el.find('.ks_lb_select').val()),
                    }
                });
                if (result.def) result.def.then(function (result) {
                    self.grid.removeWidget($el);
                    self.do_notify(
                        _t("Item Moved"),
                        _t('Selected item is moved to ' + lb_name + ' .')
                    );
                })
            } else {
                self.do_notify(
                    _t("Item Moved"),
                    _t('Selected item is moved to ' + lb_name + ' .')
                );
            }
        },

        _onKsDuplicateItemClicked: function (ev) {
            var self = this;
            var $el = this.ks_item_data[$(ev.currentTarget).data('id')].$el;
            var lb_name = $el.find('.ks_lb_select option:selected').text();
            var lb_id = parseInt($el.find('.ks_lb_select').val());
            if ($el) {
                var result = self.trigger_up('ks_copy_item', {
                    id: parseInt($(ev.currentTarget).data('id')),
                    value: {
                        ks_leaderboard_id: lb_id,
                    }
                });
                if (result.def) result.def.then(function (result) {
                    self.do_notify(
                        _t("Item Duplicated"),
                        _t('Selected item is duplicated to ' + lb_name + ' .')
                    );
                    if(lb_id === self.ks_leaderboard_data.id) {
                        self.ksFetchAddItem(result);
                    }
                })
            }
        },


        _onKsRemoveItem: function (ev) {
            var self = this;
            var item = this.ks_item_data[$(ev.currentTarget).data('id')];

            var self = this;
            Dialog.confirm(this, (_t("Are you sure you want to remove this item?")), {
                confirm_callback: function () {

                    self._rpc({
                        model: 'ks_leaderboard.leaderboard.item',
                        method: 'unlink',
                        args: [item.ks_item_id],
                    }).then(function (result) {
                        if (result) {
                            self.grid.removeWidget(item.$el);
                        }
                    });
                },
            });

        },

        _ksRenderEditMode: function (e) {
            var self = this;
            self.ks_state.ks_edit_mode = true;
            self.ksRenderHeader();

             self.$el.addClass('ks_leaderboard_edit_mode_view');

            self.ksRemoveRefreshInterval();

            if (self.grid) {
                self.grid.enable();
            }
        },

        _ksRenderActiveMode: function () {
            var self = this;
            self.ks_state.ks_edit_mode = false;
            self.$el.removeClass('ks_leaderboard_edit_mode_view');

            self.ksSetRefreshInterval();

            self.ksRenderHeader();
            if (self.grid) {
                self.grid.disable();
            }
        },

        _ksSaveLayout: function (e) {
            var self = this;
            //        Have  to save Leaderboard here
            var lb_title = self.$el.find('#ks_lb_title_input').val();
            if (lb_title != false && lb_title.length > 0 && lb_title !== self.ks_leaderboard_data.name) {
                self.ks_leaderboard_data.name = lb_title;
                self._rpc({
                    model: 'ks_leaderboard.leaderboard',
                    method: 'write',
                    args: [self.ks_leaderboard_data.id, {
                        'name': lb_title
                    }],
                }).then(function (result) {
                    if (result) {
                        self.trigger_up('ks_update_name', {
                            ks_name: lb_title
                        });
                    };
                })
            }

            // TODO : Make this so that it only trigger when there is some change in view
            if (this.ks_item_data) self._ksSaveItemGridConfig(this.ks_item_data, this.ks_item_ids);
            self._ksRenderActiveMode();
        },


        _ksCancelLayout: function (e) {
            if (this.grid) this._ksResetGridstackPositions();
            this._ksRenderActiveMode();

        },

        _ksResetGridstackPositions: function () {
            var self = this;
            _.each(this.ks_item_data, function (item_data) {
                var el = item_data.$el;
                var grid_config = JSON.parse(item_data.ks_gridstack_config);
                self.grid.update(el, grid_config.x, grid_config.y, grid_config.width, grid_config.height)
            });
        },


        _onKsGridstackEnable: function (e) {
            this.ks_gridstack_state['active'] = true;
        },

        _onKsGridstackDisable: function (e) {
            this.ks_gridstack_state['active'] = false;
        },

        _onKsGridstackRemoved: function (e, items) {
            var self = this;
            self.ksRemoveRefreshInterval();

            _.each(items, function (gs_item) {
                var id = parseInt(gs_item.id);
                if (id) {
                    delete self.ks_item_data[id];

                    var index = self.ks_item_ids.indexOf(id);
                    if (index > -1) {
                        self.ks_item_ids.splice(index, 1);
                    }

                }
            });

            self.ksSetRefreshInterval();

            if (self.ks_item_ids.length <= 0) {
                self.$ks_lb_main_content.append($(qweb.render("ks_lb_no_view_help")));
            }

        },

        _onKsItemSearchInput: function(ev) {
            var self = this;
            if (ev.which === $.ui.keyCode.ENTER) {
                var item = self.ks_item_data[$(ev.currentTarget).data('id')];
                self.KsItemSearchCards(item, ev.target.value);
            }

        },

        KsItemSearchCards: function(ks_item, search_input){
            var self = this;
            if(search_input === "") {
                self.KsRemoveSearchContainer(ks_item.$el);
            }else {
                KsLbApi._render_lb_item_search_box(ks_item, search_input);
            }
        },

        _onKsRemoveSearchContainer: function(ev) {
            var self = this;
            var item_el = self.ks_item_data[$(ev.currentTarget).data('id')].$el;
            self.KsRemoveSearchContainer(item_el);
            item_el.find(".ks_lb_item_configs").addClass("ks_lb_slide_up");

        },

        KsRemoveSearchContainer: function($item_el) {
            $item_el.find('.ks_lb_item_search_box').removeClass('open');
            $item_el.find('.ks_remove_search_container').addClass('ks_lb_hidden');
            $item_el.find('.ks_item_search_card_input').val("");
        },

    });

    return LeaderboardRenderer;

});