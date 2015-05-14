$(function(){
  if ($('body.portaltype-glossary').length == 0  &&
      $('body.portaltype-term').length     == 0) {
    $('#content').glossarizer({
      sourceURL: '@@glossary',
      callback: function() {
        // Callback fired after glossarizer finishes its job
        new tooltip();
      }
    });
  }
});
