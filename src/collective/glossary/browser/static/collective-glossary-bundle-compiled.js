//
// Author : http://osvaldas.info/elegant-css-and-jquery-tooltip-responsive-mobile-friendly
//

define('collective-glossary-tooltip', [
  'jquery',
], function($) {

  'use strict';

  function ToolTip (){
    var targets = $( '.glossarizer_replaced' ),
    target  = false,
    tooltip = false,
    title   = false;

    targets.bind( 'mouseenter', function() {
      target  = $( this );
      tip     = target.attr( 'title' );
      tooltip = $( '<div id="tooltip"></div>' );

      if( !tip || tip == '' )
        return false;

      target.removeAttr( 'title' );
      tooltip.css( 'opacity', 0 )
        .html( tip )
        .appendTo( 'body' );

      var init_tooltip = function()
      {
        if( $( window ).width() < tooltip.outerWidth() * 1.5 )
          tooltip.css( 'max-width', $( window ).width() / 2 );
        else
          tooltip.css( 'max-width', 340 );

        var pos_left = target.offset().left + ( target.outerWidth() / 2 ) - ( tooltip.outerWidth() / 2 ),
        pos_top  = target.offset().top - tooltip.outerHeight() - 20;

        if( pos_left < 0 )
        {
          pos_left = target.offset().left + target.outerWidth() / 2 - 20;
          tooltip.addClass( 'left' );
        }
        else
          tooltip.removeClass( 'left' );

        if( pos_left + tooltip.outerWidth() > $( window ).width() )
        {
          pos_left = target.offset().left - tooltip.outerWidth() + target.outerWidth() / 2 + 20;
          tooltip.addClass( 'right' );
        }
        else
          tooltip.removeClass( 'right' );

        if( pos_top < 0 )
        {
          var pos_top  = target.offset().top + target.outerHeight();
          tooltip.addClass( 'top' );
        }
        else
          tooltip.removeClass( 'top' );

        tooltip.css( { left: pos_left, top: pos_top } )
          .animate( { top: '+=10', opacity: 1 }, 50 );
      };

      init_tooltip();
      $( window ).resize( init_tooltip );

      var remove_tooltip = function()
      {
        tooltip.animate( { top: '-=10', opacity: 0 }, 50, function()
                         {
                           $( this ).remove();
                         });

        target.attr( 'title', tip );
      };

      target.bind( 'mouseleave', remove_tooltip );
      tooltip.bind( 'click', remove_tooltip );
    });
  }

  return ToolTip;
});

/**
 * Plugin Name: Glossarizer
 * Author : Vinay @Pebbleroad
 * Date: 02/04/2013
 * Description: Takes glossary terms from a JSON object -> Searches for terms in your html -> Wraps a abbr tag around the matched word
 * 1. Fixed IE8 bug where whitespace get removed - Had to change `abbr` tag to a block element `div`
 */

define('collective-glossary-jquery-glossarize', [
  'jquery',
], function($){

  'use strict';

  /**
   * Defaults
   */
  var pluginName = 'glossarizer',
  defaults = {
    sourceURL     : '', /* URL of the JSON file with format {"term": "", "description": ""} */
    replaceTag    : 'abbr', /* Matching words will be wrapped with abbr tags by default */
    lookupTagName : 'p, ul, a, div', /* Lookup in either paragraphs or lists. Do not replace in headings */
    callback      : null, /* Callback once all tags are replaced: Call or tooltip or anything you like */
    replaceOnce   : false /* Replace only once in a TextNode */,
    replaceClass: 'glossarizer_replaced'
  }

  /**
   * Constructor
   */
  function Glossarizer(el, options){
    var base = this
    base.el = el;

    /* Element */
    base.$el = $(el)

    /* Extend options */
    base.options = $.extend({}, defaults, options)

    /* Terms */
    base.terms = [];

    /* Excludes array */
    base.excludes = [];

    /* Replaced words array */
    base.replaced = [];

    /* Regex Tags */
    base.regexOption = base.options.replaceOnce? 'i': 'ig';

    /* Fetch glossary JSON */
    $.getJSON(this.options.sourceURL).then(function(data){
      base.glossary = data;

      if(!base.glossary.length || base.glossary.length == 0) return;

      /**
       * Get all terms
       */
      for (var i =0; i< base.glossary.length; i++){
        var terms = base.glossary[i].term.split(',');

        for(var j = 0; j < terms.length; j++){
          /* Trim */
          var trimmed = terms[j].replace(/^\s+|\s+$/g, ''),
          isExclusion = trimmed.indexOf('!');

          if(isExclusion == -1 || isExclusion != 0){
            /* Glossary terms array */
            base.terms.push(trimmed)
          } else {
            /* Excluded terms array */
            base.excludes.push(trimmed.substr(1));
          }
        }
      }

      /**
       * Wrap terms
       */
      base.wrapTerms();
    })
  }

  /**
   * Prototypes
   */
  Glossarizer.prototype = {
    getDescription: function(term){
      var regex = new RegExp('(^\s*)'+this.clean(term)+'\\s*|\\,$', 'i');

      /**
       * Matches
       * 1. Starts with \s* (zero or more spaces)
       * 2. Ends with zero or more spaces
       * 3. Ends with comma
       */
      for(var i =0; i< this.glossary.length; i++){
        if(this.glossary[i].term.match(regex)){
          return this.glossary[i].description.replace(/\"/gi, '&quot;')
        }
      }

    },

    clean: function(text){
      var reEscape = new RegExp('(\\' + ['/', '.', '*', '+', '?', '(', ')', '[', ']', '{', '}', '\\'].join('|\\') + ')', 'g')
      return text.replace(reEscape, '\\$1')
    },

    /**
     * Wraps the matched terms by calling traverser
     */
    wrapTerms: function(){
      this.cleanedTerms = this.clean(this.terms.join('|'))
      this.excludedTerms = this.clean(this.excludes.join('|'))
      var nodes = this.el.querySelectorAll(this.options.lookupTagName)

      for(var i =0; i < nodes.length; i++){
        this.traverser(nodes[i])
      }

      /**
       * Callback
       */

      if(this.options.callback) this.options.callback.call(this.$el)
    },

    /**
     * Traverses through nodes to find the matching terms in TEXTNODES
     */
    traverser: function(node){
      var next,
      base = this;

      if (node.nodeType === 1) {
        /*
          Element Node
        */
        if (node = node.firstChild) {
          do {
            // Recursively call traverseChildNodes
            // on each child node
            next = node.nextSibling

            /**
             * Check if the node is not glossarized
             */
            if (node.className != this.options.replaceClass)
            {
              this.traverser(node)
            }
          } while(node = next)
        }
      } else if (node.nodeType === 3) {
        /*
          Text Node
        */
        /* Plone 5 hack: do not mess with Tinymce internal buffer */
        if (node.parentNode.name == 'form.widgets.IRichText.text') return;
        var temp = document.createElement('div'),
        data = node.data;
        var re = new RegExp('(?:^|\\b)('+this.cleanedTerms+ ')(?!\\w)', base.regexOption),
        reEx = new RegExp('(?:^|\\b)('+this.excludedTerms+ ')(?!\\w)', base.regexOption);

        if(re.test(data)){
          var excl = reEx.exec(data);

          data = data.replace(re,function(match, item , offset, string) {

            if(base.options.replaceOnce && inArrayIn(match, base.replaced) >= 0){
              return match;
            }

            base.replaced.push(match);
            var ir = new RegExp('(?:^|\\b)'+base.clean(match)+'(?!\\w)'),
            result = ir.exec(data)

            if(result){
              if(excl && base.excludes.length){
                var id = offset,
                exid = excl.index,
                exl = excl.index + excl[0].length;

                if(exid <= id && id <= exl){
                  return match;
                }else{
                  return '<'+base.options.replaceTag+' class="'+base.options.replaceClass+'" title="'+base.getDescription(match)+'">'+ match + '</'+base.options.replaceTag+'>'
                }
              }
              else{
                return '<'+base.options.replaceTag+' class="'+base.options.replaceClass+'" title="'+base.getDescription(match)+'">'+ match + '</'+base.options.replaceTag+'>'
              }
            }
          });

          /**
           * Only replace when a match is found
           * Resorting to jQuery html() because of IE8 whitespace issue.
           * IE 8 removes leading whitespace from Text Nodes. Hence innerhtml doesnt work.
           *
           */
          $(temp).html(data)

          while (temp.firstChild) {
            node.parentNode.insertBefore(temp.firstChild, node)
          }

          node.parentNode.removeChild(node)
        }
      }
    },
  };

  /**
   * Public Methods
   */
  var methods = {
    destroy: function() {
      this.$el.removeData('plugin_' + pluginName);

      /* Remove abbr tag */
      this.$el.find('.' + this.options.replaceClass).each(function(){
        var $this = $(this),
        text = $this.text();

        $this.replaceWith(text);
      });
    }
  }

  /**
   * Extend Prototype
   */
  Glossarizer.prototype = $.extend({}, Glossarizer.prototype, methods)

  /**
   * Plugin
   * @param  {[type]} options
   */
  $.fn[pluginName] =function(options){
    return this.each(function(){
      var $this = $(this),
      glossarizer = $this.data('plugin_' + pluginName);

      /*
        Check if its a method
      */
      if(typeof options == "string" && glossarizer  && methods.hasOwnProperty(options) ){
        glossarizer[options].apply(glossarizer)
      }else{
        /* Destroy if exists */
        if(glossarizer) glossarizer['destroy'].apply(glossarizer);

        /* Initialize */
        $.data(this, 'plugin_' + pluginName, new Glossarizer(this, options))
      }
    });
  }

  /**
   * In Array
   */
  function inArrayIn(elem, arr, i){
    if (typeof elem !== 'string'){
      return $.inArray.apply(this, arguments);
    }

    if (arr){
      var len = arr.length;
      i = i ? (i < 0 ? Math.max(0, len + i) : i) : 0;
      elem = elem.toLowerCase();
      for (; i < len; i++){
        if (i in arr && arr[i].toLowerCase() == elem){
          return i;
        }
      }
    }
    return -1;
  }
});

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

/* initialize plugins */
require([
    // IMPORTANT: this is the name of the pattern registered in plone.resourceregistry
    'collective-glossary-main',
], function($){
    'use strict';
});

define("/home/daggelpop/projects/apef/buildout.apef.tutorat/src/collective.glossary/src/collective/glossary/browser/static/bundle.js", function(){});

