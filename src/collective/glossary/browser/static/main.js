$(function(){
  $('#content-core').glossarizer({
    sourceURL: '@@glossary',
    callback: function() {
      // Callback fired after glossarizer finishes its job
      new tooltip();
    }
  });
});
