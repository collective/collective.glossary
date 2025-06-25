# collective.glossary

Plone backend add-on to define a glossary and provide tooltips on matching text.

## Features

- The terms are defined as title / definition pairs.
- The term can have variants.
- The definiton is richtext formated.
- The tooltip can be disabled in glossary control panel.
- Tooltips can be restricted to a selection of content types.

The add-on provides a REST API service @glossary_terms to fetch the terms of the glossary.

`@rohberg/volto-slate-glossary <https://github.com/rohberg/volto-slate-glossary>`_ is the corresponding Volto add-on.

## Installation

Install collective.glossary with `pip`:

```shell
pip install collective.glossary
```

And to create the Plone site:

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/collective/collective.glossary/issues)
- [Source code](https://github.com/collective/collective.glossary/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.glossary.git
    cd collective.glossary
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Add features using `plonecli` or `bobtemplates.plone`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To run `plonecli` with configuration to target this package, run the following command.

```shell
make add <template_name>
```

For example, you can add a content type to your package with the following command.

```shell
make add content_type
```

You can add a behavior with the following command.

```shell
make add behavior
```

```{seealso}
You can check the list of available subtemplates in the [`bobtemplates.plone` `README.md` file](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates).
See also the documentation of [Mockup and Patternslib](https://6.docs.plone.org/classic-ui/mockup.html) for how to build the UI toolkit for Classic UI.
```

## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (0.9.7)](https://github.com/plone/cookieplone) and [cookieplone-templates (c7497ac)](https://github.com/plone/cookieplone-templates/commit/c7497ace6a6d52fd75e67047f652a801b03c12c4) on 2025-06-25 15:56:13.999992. A special thanks to all contributors and supporters!
