define([
  'jquery',
  'underscore',
  'backbone'
], function($, _, Backbone) {
  'use strict';
  var UserModel = Backbone.Model.extend({
    defaults: {
      'id': null,
      'organization': null,
      'name': null,
      'type': null,
      'status': null,
      'virt_addresses': null
    },
    url: function() {
      var url = '/user/' + this.get('organization');

      if (this.get('id')) {
        url += '/' + this.get('id');
      }

      return url;
    }
  });

  return UserModel;
});
