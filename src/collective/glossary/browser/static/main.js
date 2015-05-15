$(function(){
  $('#content').glossarizer({
    sourceURL: '@@glossary',
    callback: function() {
      // Callback fired after glossarizer finishes its job
      new tooltip();
    }
  });
});
