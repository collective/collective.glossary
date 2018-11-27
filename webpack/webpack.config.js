const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  'collective.glossary',
  'glossary',
  `${__dirname}/../src/collective/glossary/browser/static`,
  '++resource++collective.glossary/',
);
