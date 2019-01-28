// Plone 5 does not include global variables anymore
var portal_url = (portal_url === undefined) ? $('body').attr('data-portal-url') : portal_url;

$(function(){
  $('main,#content-core').glossarizer({
    sourceURL: portal_url + '/@@glossary',
    callback: function() {
      // Callback fired after glossarizer finishes its job
      new tooltip();
    }
  });
});
