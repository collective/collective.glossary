$(function(){
  $('#content-core').glossarizer({
    sourceURL: portal_url + '/@@glossary',
    callback: function() {
      // Callback fired after glossarizer finishes its job
      new tooltip();
    }
  });
});
