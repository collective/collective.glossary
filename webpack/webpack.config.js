const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  //name
  'collective.glossary',

  //shortName
  'glossary',

  //path
  `${__dirname}/../src/collective/glossary/browser/static`,

  //publicPath
  '++resource++collective.glossary/',

  //callback
  (config, options) => {
    config.entry.unshift(
      './app/img/glossary-icon.png',
    );
  },
);
