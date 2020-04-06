odoo.define('ks_leaderboard.item_preview_widget', function (require) {
    'use strict';

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var core = require('web.core');

    var KsLbApi = require('ks_leaderboard.ks_leaderboard_api');

    var QWeb = core.qweb;

    var KsLeaderboardItemPreview = AbstractField.extend({
        //    className: 'o_field_iap_credit_checker',

        //    cssLibs: [],
        //    jsLibs: [],
        //    events: {
        //        'keydown': '_onKeydown',
        //    },
        //    custom_events: {
        //        navigation_move: '_onNavigationMove',
        //    },

        fieldDependencies: {
            //        name: {type: 'char'},
            ks_model_id: {
                type: 'many2one',
                string: "Model"
            },
            ks_group_by_field_id: {
                type: 'many2one',
                string: "Group By"
            },
            ks_group_by_field_type: {
                type: 'selection',
                string: "Group By Field Type"
            },
            ks_group_by_date_selection: {
                type: 'selection',
                string: "Group By Date"
            },
            ks_ranking_field_id: {
                type: 'many2one',
                string: "Ranking Field"
            },
            ks_item_image_field_id: {
                type: 'many2one',
                string: "Image Field"
            },
            ks_item_image_relation_field_id: {
                type: 'many2one',
                string: "Image Relation Field"
            },

            ks_date_filter_field_id: {
                type: 'many2one',
                string: "Date Filter Field"
            },

            ks_ranking_order: {
                type: 'selection',
                string: "Ranking Order"
            },

            ks_target_enabled: {
                type: 'selection',
                string: "Set Target"
            },

            ks_target_value: {
                type: 'float',
                string: "Target Value"
            },

            ks_domain: {
                type: 'char',
                string: "Domain"
            },
            // count: {type: 'integer', string:"Count"},
            ks_allow_grouping: {
                type: 'boolean',
                string: "Use Grouping"
            },

            // Display Related Fields
            ks_header_layout_display: {
                type: 'selection',
                string: "Header Layout"
            },
            ks_body_layout_display: {
                type: 'selection',
                string: "Body Layout"
            },
            ks_item_theme_display: {
                type: 'selection',
                string: "Item Theme"
            },

            ks_refresh_rate: {
                type: 'selection',
                string: "Refresh Interval"
            },

            ks_date_filter_selection: {
                type: 'selection',
                string: "Date Filter Selection"
            },

            ks_item_theme_gradient: {
                type: 'boolean',
                string: "Use Gradient"
            },

            name: {
                type: 'char',
                string: "Name"
            },

            ks_item_start_date: {
                type: 'datetime',
                string: "Start Date"
            },

            ks_item_end_date: {
                type: 'datetime',
                string: "End Date"
            },
        },

        resetOnAnyFieldChange: true,


        init: function (parent, data, options) {
            this._super.apply(this, arguments);
            this.ks_required_field_list = ['ks_model_id', 'ks_ranking_field_id', 'ks_ranking_order', 'ks_header_layout_display', 'ks_body_layout_display', 'ks_item_theme_display', 'ks_refresh_rate', 'ks_date_filter_selection'];
        },


        //TODO : Only do rpc if field required is changed later using last value of fields.
        _render: function () {
            var self = this;
            self.$el.empty();
            var local_fields_required = self._ks_check_required_list(self.recordData, self.ks_required_field_list);
            var fields_required_list = local_fields_required.filter((x) => {
                return self.recordData[x] === false
            }).map((x) => {
                return self.fieldDependencies[x]['string']
            })

            if (fields_required_list.length === 0) {
                self._rpc({
                    route: '/ks_leaderboard/ks_leaderboard_item_data',
                    params: {
                        ks_model_id: [self.recordData.ks_model_id.data.id, self.recordData.ks_model_id.data.display_name],
                        ks_ranking_field_id: [self.recordData.ks_ranking_field_id.data.id, self.recordData.ks_ranking_field_id.data.display_name],
                        ks_group_by_field_id: self.recordData.ks_group_by_field_id ? [self.recordData.ks_group_by_field_id.data.id, self.recordData.ks_group_by_field_id.data.display_name] : false,
                        ks_date_filter_field_id: self.recordData.ks_date_filter_field_id ? [self.recordData.ks_date_filter_field_id.data.id, self.recordData.ks_date_filter_field_id.data.display_name] : false,
                        ks_item_image_field_id: self.recordData.ks_item_image_field_id ? [self.recordData.ks_item_image_field_id.data.id, self.recordData.ks_item_image_field_id.data.display_name] : false,
                        ks_item_image_relation_field_id: self.recordData.ks_item_image_relation_field_id ? [self.recordData.ks_item_image_relation_field_id.data.id, self.recordData.ks_item_image_relation_field_id.data.display_name] : false,
                        ks_ranking_order: self.recordData.ks_ranking_order || false,
                        ks_group_by_field_type: self.recordData.ks_group_by_field_type || false,
                        ks_group_by_date_selection: self.recordData.ks_group_by_date_selection || false,
                        ks_record_limit: self.recordData.ks_record_limit || 0,
                        ks_domain: self.recordData.ks_domain || false,
                        name: self.recordData.name || false,
                        ks_allow_grouping: self.recordData.ks_allow_grouping || false,
                        // Display Props
                        ks_header_layout_display: self.recordData.ks_header_layout_display || false,
                        ks_body_layout_display: self.recordData.ks_body_layout_display || false,
                        ks_item_theme_display: self.recordData.ks_item_theme_display || false,
                        ks_item_theme_gradient: self.recordData.ks_item_theme_gradient || false,
                        ks_refresh_rate: self.recordData.ks_refresh_rate || false,
                        ks_date_filter_selection: self.recordData.ks_date_filter_selection || false,
                        ks_item_start_date: self.recordData.ks_item_start_date || false,
                        ks_item_end_date: self.recordData.ks_item_end_date || false,
                        ks_target_enabled: self.recordData.ks_target_enabled || false,
                        ks_target_value: self.recordData.ks_target_value || 0,
                    },
                }).then(function (data) {
                    var $item_view = KsLbApi.render_lb_item_preview(data, {
                        ks_is_preview: true
                    });
                    $item_view.appendTo(self.$el);
                })
            } else {
                var $widget = $(QWeb.render('ks_item_invalid_view', {
                    field_required: fields_required_list
                }));
                $widget.appendTo(this.$el);
            }


        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------


        _ks_check_required_list: function (data, field_list) {
            //Here conditions are being checked if there is any other required field (when grouping or when selecting other fields)
            var temp_field_list = [];

            // Groupby Requird condition based on boolean field "ks_allow_grouping"
            if (data['ks_allow_grouping']) {
                temp_field_list.push("ks_group_by_field_id");
            }

            //        Date Selection Field Condition
            if (data['ks_group_by_field_type'] && ['date', 'datetime'].includes(data['ks_group_by_field_type'])) {
                temp_field_list.push("ks_group_by_date_selection")
            }
            return [].concat(temp_field_list, field_list);

        },


    });

    registry.add('ks_leaderboard_item_preview', KsLeaderboardItemPreview);

    return KsLeaderboardItemPreview;
});
