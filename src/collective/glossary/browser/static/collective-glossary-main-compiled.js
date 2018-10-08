define('collective-glossary-main', [
  'jquery',
  'collective-glossary-tooltip',
  'collective-glossary-jquery-glossarize'
], function($, tooltip) {

    'use strict';

    debugger;

    var portal_url;

    $(function () {
        // Plone 5 does not include global variables anymore
        var myp = (portal_url === undefined) ? $('body').attr('data-portal-url') : portal_url;

        $('#content-core').glossarizer({
            sourceURL: myp + '/@@glossary',
            callback: function () {
                // Callback fired after glossarizer finishes its job
                new tooltip();
            }
        });
    });

});

define("/home/daggelpop/projects/apef/buildout.apef.tutorat/src/collective.glossary/src/collective/glossary/browser/static/main.js", function(){});

