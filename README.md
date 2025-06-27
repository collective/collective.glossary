# collective.glossary

Plone backend add-on to define a glossary and provide tooltips on matching text.

## Features

- The terms are defined as title / definition pairs.
- The term can have variants.
- The definiton is richtext formated.
- The tooltip can be disabled in glossary control panel.
- Tooltips can be restricted to a selection of content types.
- REST API service @glossary_terms to fetch the terms of a glossary.

[@rohberg/volto-slate-glossary](https://github.com/rohberg/volto-slate-glossary>) is the corresponding Volto add-on.



## Screenshots

![Create a Glossary](https://raw.github.com/collective/collective.glossary/master/docs/glossary.png)

*Create a Glossary.*

![Use it!](https://raw.github.com/collective/collective.glossary/master/docs/usage.png)

*Use it!*

![Control Panel](https://raw.github.com/collective/collective.glossary/master/docs/controlpanel.png)

*Configure glossary settings in the control panel.*


## Contribute

- [Issue tracker](https://github.com/collective/collective.glossary/issues)
- [Source code](https://github.com/collective/collective.glossary/)
- [pypi](https://pypi.org/project/collective.glossary/)

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


## License

The project is licensed under GPLv2.

## Acknowledgements

Generated using [Cookieplone (0.9.7)](https://github.com/plone/cookieplone) and [cookieplone-templates (c7497ac)](https://github.com/plone/cookieplone-templates/commit/c7497ace6a6d52fd75e67047f652a801b03c12c4) on 2025-06-25 15:56:13.999992.
