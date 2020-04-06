odoo.define('ks_leaderboard.ks_leaderboard_model', function (require) {
"use strict";


var AbstractModel = require('web.AbstractModel');
var BasicModel = require('web.BasicModel');

var LeaderboardModel = AbstractModel.extend({

     init: function () {
        this._super.apply(this, arguments);
        this.local_data = {};
    },


    /**
     * Main entry point, the goal of this method is to fetch and process all
     * data (following relations if necessary) for a given record/list.
     *
     *
     * @param {any} params
     * @param {string} [params.res_id] an ID for an existing resource.
     * @returns {Deferred<string>} resolves to a local id, or handle
     */
    load: function (params) {
        var self = this;
        if (params.res_id && params.res_id>0){
            return self._rpc({
                route: '/ks_leaderboard/ks_leaderboard_data',
                params: {
                    ks_res_id: params.res_id || false,
                },
            }).then(function(data) {
                var handle = data.handle;
                self.local_data[handle] = data;
                return data;
            })
        }else{
            return $.when();
        }

    },

    /**
     * This method should return the complete state necessary for the renderer
     * to display the currently viewed data.
     *
     * @returns {*}
     */
    get: function (token) {
        if(token && this.local_data.hasOwnProperty(token)) return this.local_data[token];
    },


    reload: function(cp_handle, params){
        var self = this;
        if(params.ks_reload_status) return self[params.ks_reload_status](params.ks_lb_id);
        else return this._super.apply(this,arguments);
    },

    ks_update_all_item: function(res_id){
        var self = this;
        if (res_id && res_id>0){
            return self._rpc({
                route: '/ks_leaderboard/ks_leaderboard_data',
                params: {
                    ks_res_id: res_id || false,
                },
            }).then(function(data) {
                var handle = data.handle;
                self.local_data[handle] = data;
                return handle;
            })
        }else{
            return $.when();
        }

    },

});

return LeaderboardModel;

});