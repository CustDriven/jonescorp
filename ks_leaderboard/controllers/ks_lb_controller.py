# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, tools,fields
from odoo.http import request
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from . import ks_date_filter_selections



class KsLeaderBoardController(http.Controller):

    @http.route('/ks_leaderboard/ks_leaderboard_data', auth='user', type='json')
    def ks_leaderboard_data(self, ks_res_id):
        """
        Fetch leaderboard data with its item.
        :param ks_res_id: integer
        :return: dict
        """
        ks_model = request.env["ks_leaderboard.leaderboard"]
        ks_leaderboard_data = {}

        fields = ['name', 'ks_leaderboard_item_ids']
        record = ks_model.search_read(domain=[['id', '=', ks_res_id]], fields=fields, limit=1)
        if record and len(record) == 1:
            ks_leaderboard_data['data'] = record[0]

            if record[0]['ks_leaderboard_item_ids']:
                ks_leaderboard_data['item_data'] = self.ks_leaderboard_fetch_items_data(
                    record[0]['ks_leaderboard_item_ids'])

        # Update dict in bunch later
        ks_leaderboard_data['handle'] = "ks_leaderboard.leaderboard_" + str(ks_res_id)
        ks_leaderboard_data['res_id'] = ks_res_id
        ks_leaderboard_data['ks_lb_list'] = ks_model.search_read(fields=['id', 'name'])
        ks_leaderboard_data['ks_lb_manager'] = request.env.user.has_group('ks_leaderboard.ks_leaderboard_manager_group')

        return ks_leaderboard_data

    @http.route('/ks_leaderboard/ks_lb_fetch_items_data', auth='user', type='json')
    def ks_leaderboard_fetch_items_data(self, ks_items_ids):
        """

        :param ks_items_ids:list[int..]
        :return: dict {item_id : {item_data}}
        """
        ks_lb_items_data = {}

        ks_items_data = request.env["ks_leaderboard.leaderboard.item"].search_read(domain=[['id', 'in', ks_items_ids]])

        for item_data in ks_items_data:
            ks_lb_items_data[item_data['id']] = self.ks_leaderboard_item_data(**item_data)
            ks_lb_items_data[item_data['id']]['ks_gridstack_config'] = item_data['ks_gridstack_config']
            ks_lb_items_data[item_data['id']]['ks_item_id'] = item_data['id']
        return ks_lb_items_data

    @http.route('/ks_leaderboard/ks_leaderboard_item_data', auth='user', type='json')
    def ks_leaderboard_item_data(self, **kwargs):
        """
        Returns data of item after performing calculation.
        Note : This function is not validating any fields except Grouping Fields.
        :param kwargs: dict
        :return: dict
        """
        ks_item_data = {}
        domain = self.ks_convert_to_proper_domain(**kwargs)

        currency_id = request.env.user.company_id.currency_id.id

        # Note : Not using .get here because it is confirmed that these fields are present
        if kwargs['ks_allow_grouping'] and kwargs['ks_group_by_field_id']:
            ks_item_data.update(self.ks_leaderboard_grouped_item_data(domain, **kwargs))
        else:
            ks_item_data.update(self.ks_leaderboard_ungrouped_item_data(domain, **kwargs))

        ks_item_data.update(self.ks_lb_display_data(**kwargs))
        ks_item_data['ks_currency_id'] = currency_id

        return ks_item_data

    def ks_convert_to_proper_domain(self, **kwargs):
        # Domain Fetch
        domain = []
        if kwargs.get('ks_domain', False):
            domain = eval(kwargs['ks_domain'])

        if kwargs.get('ks_date_filter_field_id', False):
            ks_date_filter_field_id = request.env['ir.model.fields'].browse([kwargs.get('ks_date_filter_field_id')[0]])

            ks_date_filter_selection = kwargs.get('ks_date_filter_selection', False)

            ks_date_domain = False

            selected_start_date = selected_end_date = False

            if not ks_date_filter_selection or ks_date_filter_selection == "l_none":
                pass
                # TODO : dashboard on fly date filter code here
                # selected_start_date = self._context.get('ksDateFilterStartDate', False)
                # selected_end_date = self._context.get('ksDateFilterEndDate', False)
                # if selected_start_date and selected_end_date and rec.ks_date_filter_field.name:
                #     ks_date_domain = [
                #         (rec.ks_date_filter_field.name, ">=",
                #          selected_start_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                #         (rec.ks_date_filter_field.name, "<=",
                #          selected_end_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))]
            else:
                if ks_date_filter_selection and ks_date_filter_selection != 'l_custom':
                    ks_df_selection = ks_date_filter_selections.KsDateFilterSelection()
                    ks_date_data = ks_df_selection.ks_date_filter_selection(ks_date_filter_selection)

                    selected_start_date = fields.datetime.strftime(ks_date_data["selected_start_date"], DEFAULT_SERVER_DATETIME_FORMAT)
                    selected_end_date = fields.datetime.strftime(ks_date_data["selected_end_date"], DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    selected_start_date = kwargs.get('ks_item_start_date', False)
                    selected_end_date = kwargs.get('ks_item_end_date', False)

                if selected_start_date and selected_end_date :
                    ks_date_domain = [(ks_date_filter_field_id.name, ">=", selected_start_date),
                                      (ks_date_filter_field_id.name, "<=", selected_end_date)]

            if ks_date_domain:
                domain.extend(ks_date_domain)

        return domain

    def ks_lb_display_data(self, **kwargs):
        """
        Adding Display Properties in Item Info
        :param kwargs:
        :return: dict {'display':{}}
        """
        return {'display': {'ks_header_layout_display': kwargs['ks_header_layout_display'],
                            'ks_body_layout_display': kwargs['ks_body_layout_display'],
                            'ks_item_theme_display': kwargs.get('ks_item_theme_display', False),
                            'ks_item_theme_gradient': kwargs.get('ks_item_theme_gradient', False)
                            },
                'ks_item_name': kwargs.get('name', False) if kwargs.get('name', False) else kwargs.get('ks_model_id')[1],
                'ks_refresh_rate': kwargs.get('ks_refresh_rate', 60),
                }


    def ks_leaderboard_ungrouped_item_data(self, domain, **kwargs):
        """

        :param kwargs:
        :return:
        """

        # TODO : Later have to send res_id and model to handle item card click
        # TODO : need domain, fields to read list/show, image_field

        ks_item_data = {}
        field_list = ['name']

        ir_model = request.env['ir.model'].browse([kwargs.get('ks_model_id')[0]])

        ir_field = request.env['ir.model.fields'].browse([kwargs.get('ks_ranking_field_id')[0]])
        ks_item_data['rank_field'] = ir_field.name
        field_list.append(ir_field.name)

        # Image Field Fetch
        ks_item_data['ks_image_field'] = False
        if kwargs.get('ks_item_image_field_id', False):
            ir_image_field = request.env['ir.model.fields'].browse([kwargs.get('ks_item_image_field_id')[0]])
            field_list.append(ir_image_field.name)
            ks_item_data['ks_image_field'] = ir_image_field.name

        ks_item_data['ks_target_enabled'] = kwargs.get('ks_target_enabled', False)
        ks_item_data['ks_target_value'] = kwargs.get('ks_target_value', 0.0)

        # Domain Fetch
        # if kwargs.get('ks_domain', False):
        #     domain = eval(kwargs['ks_domain'])

        order = kwargs.get('ks_ranking_order', False)
        limit = kwargs.get('ks_record_limit', False)

        # read is low-level rpc. therefore important to set limit to reduce overload. Might shift this into read case
        limit = limit if limit < 20 else 20

        ks_item_cards_data = []
        """
        item_cards_data_structure = [{
            'rank_field': {'value':xx,'string':'some_label','type':_type},
            'image': binary data of image {later},
            'field_to_show_1' : {'value':xx,'name':'some_label','type':_type},
            'rec_id': in search read case
        },{},...]
        """
        ks_item_data['other_fields_list'] = ['name']

        fields_info = request.env[ir_model.model].fields_get(allfields=field_list+['display_name'],
                                                             attributes=['string', 'type', 'currency_field'])
        try:
            records = request.env[ir_model.model].search_read(domain, order=ir_field.name + " " + order, limit=limit,
                                                              fields=field_list+['display_name'])
        except Exception as e:
            ks_item_data['item_cards'] = []
            return ks_item_data

        for index, rec in enumerate(records):
            data = {}
            for field in field_list:
                data[field] = fields_info[field].copy() if field in fields_info else fields_info['display_name'].copy()

                if data[field]['type'] == 'binary':
                    data[field]['value'] = tools.image_data_uri(rec[field]) if rec[
                        field] else "/web/static/src/img/placeholder.png"
                else:
                    data[field]['value'] = rec[field] if field in rec else rec['display_name']

                # if data[field].get('currency_field', False):
                #     data[field]['currency_id'] = currency_id

            data['rec_id'] = rec['id']
            data['ks_rank'] = index + 1
            if ks_item_data['ks_target_enabled']:
                rank_value = data[ks_item_data['rank_field']]['value']
                target_value = ks_item_data['ks_target_value']

                max_value = target_value if target_value >= rank_value else rank_value
                target_achieved = True if rank_value >= target_value else False
                success_value = rank_value if rank_value <= target_value else target_value
                success_per = 0.0
                diff_value = max_value - success_value
                diff_per = 0.0

                if max_value:
                    diff_per = diff_value/max_value * 100
                    success_per = 100 - diff_per

                data['ks_target_status'] = {
                    'target_achieved': target_achieved,
                    'success_value': success_value,
                    'success_per': round(success_per,2),
                    'diff_value': diff_value,
                    'diff_per': round(diff_per,2),
                }

            ks_item_cards_data.append(data)

        ks_item_data['item_cards'] = ks_item_cards_data

        return ks_item_data

    def ks_leaderboard_grouped_item_data(self, domain, **kwargs):
        ks_item_data = {}

        # Making Chain ifs to compute 4 different group read cases
        if kwargs['ks_group_by_field_type'] == "many2one":
            return self.ks_gr_many2one_data(domain, **kwargs)
        elif kwargs['ks_group_by_field_type'] in ["date", "datetime"]:
            return self.ks_gr_date_data(domain, **kwargs) if kwargs['ks_group_by_date_selection'] else {}
        elif kwargs['ks_group_by_field_type'] == "selection":
            return self.ks_gr_selection_data(domain, **kwargs)
        else:
            return self.ks_gr_other_data(domain, **kwargs)

    def ks_gr_many2one_data(self, domain, **kwargs):
        ks_item_data = {}
        field_list = []
        group_by_field_list = []

        ir_model = request.env['ir.model'].browse([kwargs.get('ks_model_id')[0]])

        ir_field = request.env['ir.model.fields'].browse([kwargs.get('ks_ranking_field_id')[0]])
        ks_item_data['rank_field'] = ir_field.name
        field_list.append(ir_field.name)

        ir_group_field = request.env['ir.model.fields'].browse([kwargs['ks_group_by_field_id'][0]])
        ks_item_data['group_by_field'] = ir_group_field.name
        field_list.append(ir_group_field.name)
        group_by_field_list.append(ir_group_field.name)

        # Image Field Fetch
        ks_item_data['ks_image_field'] = False
        if kwargs.get('ks_item_image_relation_field_id', False):
            ir_image_field = request.env['ir.model.fields'].browse([kwargs.get('ks_item_image_relation_field_id')[0]])
            # field_list.append(ir_image_field.name)
            ks_item_data['ks_image_field'] = ir_image_field.name

        order = kwargs.get('ks_ranking_order', False)
        limit = kwargs.get('ks_record_limit', False)

        ks_item_data['ks_target_enabled'] = kwargs.get('ks_target_enabled', False)
        ks_item_data['ks_target_value'] = kwargs.get('ks_target_value', 0.0)

        # read is low-level rpc. therefore important to set limit to reduce overload. Might shift this into read case
        limit = limit if limit < 20 else 20

        ks_item_cards_data = []

        ks_item_data['other_fields_list'] = group_by_field_list

        fields_info = request.env[ir_model.model].fields_get(allfields=field_list,
                                                             attributes=['string', 'type', 'currency_field'])

        try:
            records = request.env[ir_model.model].read_group(domain=domain, fields=field_list,
                                                             groupby=group_by_field_list,
                                                             orderby=ir_field.name + " " + order, limit=limit)
        except Exception as e:
            ks_item_data['item_cards'] = []
            return ks_item_data

        for index, rec in enumerate(records):
            data = {}
            for field in field_list:
                data[field] = fields_info[field].copy()

                if data[field]['type'] == 'many2one':
                    data[field]['value'] = str(rec[field][1]) if rec[field] else rec[field]
                else:
                    data[field]['value'] = rec.get(field,0)

                # if data[field].get('currency_field', False):
                #     data[field]['currency_id'] = currency_id

            if ks_item_data['ks_image_field']:
                if rec[field]:
                    image_byte = request.env[ir_group_field.relation].browse(rec[field][0])[ks_item_data['ks_image_field']]
                    data[ks_item_data['ks_image_field']] = {
                        'value': tools.image_data_uri(image_byte) if image_byte else "/web/static/src/img/placeholder.png",
                    }
                else:
                    data[ks_item_data['ks_image_field']] = {
                        'value': "/web/static/src/img/placeholder.png",
                    }

            if ks_item_data['ks_target_enabled']:
                rank_value = data[ks_item_data['rank_field']]['value']
                target_value = ks_item_data['ks_target_value']

                max_value = target_value if target_value >= rank_value else rank_value
                target_achieved = True if rank_value >= target_value else False
                success_value = rank_value if rank_value <= target_value else target_value
                success_per = 0.0
                diff_value = max_value - success_value
                diff_per = 0.0

                if max_value:
                    diff_per = diff_value/max_value * 100
                    success_per = 100 - diff_per

                data['ks_target_status'] = {
                    'target_achieved': target_achieved,
                    'success_value': success_value,
                    'success_per': round(success_per,2),
                    'diff_value': diff_value,
                    'diff_per': round(diff_per,2),
                }

            data['rec_id'] = rec[field][0] if rec[field] else rec[field]
            data['ks_rank'] = index + 1
            ks_item_cards_data.append(data)

        ks_item_data['item_cards'] = ks_item_cards_data

        return ks_item_data

    def ks_gr_date_data(self, domain, **kwargs):
        ks_item_data = {}
        field_list = []
        group_by_field_list = []

        ir_model = request.env['ir.model'].browse([kwargs.get('ks_model_id')[0]])

        ir_field = request.env['ir.model.fields'].browse([kwargs.get('ks_ranking_field_id')[0]])
        ks_item_data['rank_field'] = ir_field.name
        field_list.append(ir_field.name)

        ir_group_field = request.env['ir.model.fields'].browse([kwargs['ks_group_by_field_id'][0]])
        ks_item_data['group_by_field'] = ir_group_field.name + ":" + kwargs['ks_group_by_date_selection']
        field_list.append(ir_group_field.name)
        group_by_field_list.append(ir_group_field.name + ":" + kwargs['ks_group_by_date_selection'])

        # No Image

        order = kwargs.get('ks_ranking_order', False)
        limit = kwargs.get('ks_record_limit', False)

        ks_item_data['ks_target_enabled'] = kwargs.get('ks_target_enabled', False)
        ks_item_data['ks_target_value'] = kwargs.get('ks_target_value', 0.0)

        # read is low-level rpc. therefore important to set limit to reduce overload. Might shift this into read case
        limit = limit if limit < 20 else 20

        ks_item_cards_data = []
        ks_item_data['other_fields_list'] = [ir_group_field.name]

        fields_info = request.env[ir_model.model].fields_get(allfields=field_list,
                                                             attributes=['string', 'type', 'currency_field'])

        try:
            records = request.env[ir_model.model].read_group(domain=domain, fields=field_list, groupby=group_by_field_list,
                                                             orderby=ir_field.name + " " + order, limit=limit)
        except Exception as e:
            ks_item_data['item_cards'] = []
            return ks_item_data

        for index, rec in enumerate(records):
            data = {}
            for field in field_list:
                data[field] = fields_info[field].copy()

                if field == ir_group_field.name:
                    data[field]['value'] = rec[field + ":" + kwargs['ks_group_by_date_selection']]
                else:
                    data[field]['value'] = rec.get(field,0)

                # if data[field].get('currency_field', False):
                #     data[field]['currency_id'] = currency_id

            if ks_item_data['ks_target_enabled']:
                rank_value = data[ks_item_data['rank_field']]['value']
                target_value = ks_item_data['ks_target_value']

                max_value = target_value if target_value >= rank_value else rank_value
                target_achieved = True if rank_value >= target_value else False
                success_value = rank_value if rank_value <= target_value else target_value
                success_per = 0.0
                diff_value = max_value - success_value
                diff_per = 0.0

                if max_value:
                    diff_per = diff_value/max_value * 100
                    success_per = 100 - diff_per

                data['ks_target_status'] = {
                    'target_achieved': target_achieved,
                    'success_value': success_value,
                    'success_per': round(success_per,2),
                    'diff_value': diff_value,
                    'diff_per': round(diff_per,2),
                }

            data['rec_id'] = False
            data['ks_rank'] = index + 1
            ks_item_cards_data.append(data)

        ks_item_data['item_cards'] = ks_item_cards_data

        return ks_item_data

    def ks_gr_selection_data(self,domain, **kwargs):
        ks_item_data = {}
        field_list = []
        group_by_field_list = []

        ir_model = request.env['ir.model'].browse([kwargs.get('ks_model_id')[0]])

        ir_field = request.env['ir.model.fields'].browse([kwargs.get('ks_ranking_field_id')[0]])
        ks_item_data['rank_field'] = ir_field.name
        field_list.append(ir_field.name)

        ir_group_field = request.env['ir.model.fields'].browse([kwargs['ks_group_by_field_id'][0]])
        ks_item_data['group_by_field'] = ir_group_field.name
        field_list.append(ir_group_field.name)
        group_by_field_list.append(ir_group_field.name)

        order = kwargs.get('ks_ranking_order', False)
        limit = kwargs.get('ks_record_limit', False)

        ks_item_data['ks_target_enabled'] = kwargs.get('ks_target_enabled', False)
        ks_item_data['ks_target_value'] = kwargs.get('ks_target_value', 0.0)

        # read is low-level rpc. therefore important to set limit to reduce overload. Might shift this into read case
        limit = limit if limit < 20 else 20

        ks_item_cards_data = []
        ks_item_data['other_fields_list'] = group_by_field_list


        fields_info = request.env[ir_model.model].fields_get(allfields=field_list,
                                                             attributes=['string', 'type', 'currency_field',
                                                                         'selection'])


        try:
            records = request.env[ir_model.model].read_group(domain=domain, fields=field_list, groupby=group_by_field_list,
                                                             orderby=ir_field.name + " " + order, limit=limit)

        except Exception as e:
            ks_item_data['item_cards'] = []
            return ks_item_data

        for index, rec in enumerate(records):
            data = {}
            for field in field_list:
                data[field] = fields_info[field].copy()

                if data[field]['type'] == 'selection':
                    data[field]['value'] = dict(fields_info[field]['selection'])[rec[field]] if rec[field] else False
                else:
                    data[field]['value'] = rec.get(field,0)

                # if data[field].get('currency_field', False):
                #     data[field]['currency_id'] = currency_id

            if ks_item_data['ks_target_enabled']:
                rank_value = data[ks_item_data['rank_field']]['value']
                target_value = ks_item_data['ks_target_value']

                max_value = target_value if target_value >= rank_value else rank_value
                target_achieved = True if rank_value >= target_value else False
                success_value = rank_value if rank_value <= target_value else target_value
                success_per = 0.0
                diff_value = max_value - success_value
                diff_per = 0.0

                if max_value:
                    diff_per = diff_value/max_value * 100
                    success_per = 100 - diff_per

                data['ks_target_status'] = {
                    'target_achieved': target_achieved,
                    'success_value': success_value,
                    'success_per': round(success_per,2),
                    'diff_value': diff_value,
                    'diff_per': round(diff_per,2),
                }

            data['rec_id'] = False
            data['ks_rank'] = index + 1
            ks_item_cards_data.append(data)

        ks_item_data['item_cards'] = ks_item_cards_data

        return ks_item_data

    def ks_gr_other_data(self,domain, **kwargs):
        ks_item_data = {}
        field_list = []
        group_by_field_list = []

        ir_model = request.env['ir.model'].browse([kwargs.get('ks_model_id')[0]])

        ir_field = request.env['ir.model.fields'].browse([kwargs.get('ks_ranking_field_id')[0]])
        ks_item_data['rank_field'] = ir_field.name
        field_list.append(ir_field.name)

        ir_group_field = request.env['ir.model.fields'].browse([kwargs['ks_group_by_field_id'][0]])
        ks_item_data['group_by_field'] = ir_group_field.name
        field_list.append(ir_group_field.name)
        group_by_field_list.append(ir_group_field.name)

        # Image Cannot be shown in this criteria

        order = kwargs.get('ks_ranking_order', False)
        limit = kwargs.get('ks_record_limit', False)

        ks_item_data['ks_target_enabled'] = kwargs.get('ks_target_enabled', False)
        ks_item_data['ks_target_value'] = kwargs.get('ks_target_value', 0.0)

        # read is low-level rpc. therefore important to set limit to reduce overload. Might shift this into read case
        limit = limit if limit < 20 else 20

        ks_item_cards_data = []

        # Todo : Count feature to show duplicate grouped (in upcoming feture)
        if ir_group_field.name == ir_field.name:
            # ks_item_data['other_fields_list'] = [ir_group_field.name + '_group'] + ['count']
            ks_item_data['other_fields_list'] = [ir_group_field.name + '_group']
        else:
            # ks_item_data['other_fields_list'] = group_by_field_list + ['count']
            ks_item_data['other_fields_list'] = group_by_field_list

        fields_info = request.env[ir_model.model].fields_get(allfields=field_list,
                                                             attributes=['string', 'type', 'currency_field'])

        try:
            records = request.env[ir_model.model].read_group(domain=domain, fields=field_list, groupby=group_by_field_list,
                                                             orderby=ir_field.name + " " + order, limit=limit)
        except Exception as e:
            ks_item_data['item_cards'] = []
            return ks_item_data

        for index, rec in enumerate(records):
            data = {}
            for field in set(field_list):
                data[field] = fields_info[field].copy()

                if field in group_by_field_list:
                    data[field + "_group"] = {
                        'string': data[field]['string'],
                        'type': data[field]['type'],
                        'value': rec[field],
                    }
                    data[field]['value'] = rec[field] * rec[field + "_count"]

                else:
                    data[field]['value'] = rec.get(field,0)

                # if data[field].get('currency_field', False):
                #     data[field]['currency_id'] = currency_id

            if ks_item_data['ks_target_enabled']:
                rank_value = data[ks_item_data['rank_field']]['value']
                target_value = ks_item_data['ks_target_value']

                max_value = target_value if target_value >= rank_value else rank_value
                target_achieved = True if rank_value >= target_value else False
                success_value = rank_value if rank_value <= target_value else target_value
                success_per = 0.0
                diff_value = max_value - success_value
                diff_per = 0.0

                if max_value:
                    diff_per = diff_value/max_value * 100
                    success_per = 100 - diff_per

                data['ks_target_status'] = {
                    'target_achieved': target_achieved,
                    'success_value': success_value,
                    'success_per': round(success_per,2),
                    'diff_value': diff_value,
                    'diff_per': round(diff_per,2),
                }

            data["count"] = {
                'string': "Count",
                'type': 'integer',
                'value': rec[ir_group_field.name + '_count'],
            }
            data['rec_id'] = False
            data['ks_rank'] = index + 1
            ks_item_cards_data.append(data)

        ks_item_data['item_cards'] = ks_item_cards_data

        return ks_item_data
