odoo.define('ks_leaderboard.view_registry', function (require) {
"use strict";


var AbstractView = require('web.AbstractView');
var BasicView = require('web.BasicView');
var LeaderboardController = require('ks_leaderboard.ks_leaderboard_controller');
var LeaderboardModel = require('ks_leaderboard.ks_leaderboard_model');
var LeaderboardRenderer = require('ks_leaderboard.ks_leaderboard_renderer');
var config = require('web.config');

var core = require('web.core');
var FormController = require('web.FormController');
var FormRenderer = require('web.FormRenderer');

var _lt = core._lt;


var view_registry = require('web.view_registry');

var LeaderboardView = AbstractView.extend({

    jsLibs: [
            '/ks_leaderboard/static/lib/gridstack/gridstack.min.js',
            '/ks_leaderboard/static/lib/gridstack/gridstack.jQueryUI.min.js',
        ],

//        Todo : remove uncomment file from directory
    cssLibs: [
            '/ks_leaderboard/static/lib/gridstack/gridstack.min.css',
        ],

    config: _.extend({}, BasicView.prototype.config, {
        Model: LeaderboardModel,
        Controller: LeaderboardController,
        Renderer: LeaderboardRenderer,
    }),

    display_name: _lt('Leaderboard'),
    multi_record: false,
    searchable: false,
    icon: 'fa-edit',
    viewType: 'ks_leaderboard',
    withControlPanel: false,
    display_name: 'Leaderboard',

    init: function (viewInfo, params) {
        this._super.apply(this, arguments);


//        if (config.device.isMobile) {
//            this.jsLibs.push('/web/static/lib/jquery.touchSwipe/jquery.touchSwipe.js');
//        }
    },

    _loadData: function (parent) {
        var model = this.getModel(parent);
        return model.load(this.loadParams);
    },

});


view_registry.add('ks_leaderboard', LeaderboardView);
return LeaderboardView;

});
