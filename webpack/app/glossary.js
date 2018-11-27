import './js/tooltip';
import './js/jquery.glossarize';

var portal_url = (portal_url === undefined) ? $('body').attr('data-portal-url') : portal_url;

$('#content-core').glossarizer({
    sourceURL: portal_url + '/@@glossary',
    callback: function() {
      // Callback fired after glossarizer finishes its job
      new tooltip();
    }
  });
