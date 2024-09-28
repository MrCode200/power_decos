# How to Use Sphinx for Generating HTML Documentation

## Table of Contents

- [First Time Setup Commands](#first-time-setup-commands)
- [Modify the Files to work(still First Time Setup)](#modify-the-files-to-workstill-first-time-setup)
- [Generating HTML Documentation](#generating-html-documentation)
- [Optional: Host the HTML Documentation Online](#optional-host-the-html-documentation-online)
- [Summary of Changes/Clarifications](#summary-of-changesclarifications)
- [Steps to Update the Sphinx HTML Documentation](#steps-to-update-the-sphinx-html-documentation)
- [Command Summary of Update the Sphinx HTML Documentation:](#command-summary-of-update-the-sphinx-html-documentation)

### All steps till [Optional: Host the HTML Documentation Online](#optional-host-the-html-documentation-online) and [Steps to Update the Sphinx HTML Documentation](#steps-to-update-the-sphinx-html-documentation) can be skipped by running [power_decos\.github\generate_docs.bat](./generate_docs.bat)

### First Time Setup Commands:
1. #### Initialize Sphinx:
    ```
   > cd docs
   > sphinx-quickstart
   
This command will guide you through setting up a basic conf.py, index.rst, 
and other necessary files. Answer the prompts based on your project setup.3. 

2. #### Generate Documentation Stubs for All Modules:
    Go back to your project root:

    ```
    > cd ..
    > sphinx-apidoc -o docs .
   ```
   
    This generates reStructuredText (.rst) files in the docs folder for all modules in your project.

### Modify the Files to work(still First Time Setup)
3. #### Modify the index.rst File
    Open `index.rst` inside the docs folder and modify it to include the `modules` directive:
    
    ```
   Power Decos documentation
    =========================

    .. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules # Add this line to include the module documentation
   
4. #### Modify the conf.py File:
    
    In `docs/conf.py`, add this line near the top to adjust your Python path:
    ```
   import os, sys

    sys.path.insert(0, os.path.abspath(".."))
   
5. #### Set Extensions:
    Replace the `extensions` line in `conf.py` to include the necessary Sphinx extensions:

    ```
   extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]
   
6. #### Change the HTML Theme:
    In the `conf.py` file, set the theme to `sphinx_rtd_theme` for a modern look:

    ```
    html_theme = 'sphinx_rtd_theme'
    html_static_path = ['_static']```
   
### Generating HTML Documentation
1. #### Build the HTML
   Once everything is set up, go back to the `docs` directory:
    ```
    > cd docs
    > .\make.bat html  # On Windows
    # or
    > make html        # On Unix/macOS
    ```
   This command generates the HTML documentation in the docs/_build/html/ folder. Best to move it from docs/_build/html/ to docs/html/
   
   You can open index.html in your browser to view it.
   
   NOTE: only the html folder is needed

3. #### Open Website in Browser:
    - Once created you can move the `html` folder outside of _build
    - To run the website in your local browser open the `html` file and run the `index.html`

### Optional: Host the HTML Documentation Online

1. #### Use RawGitHack for Hosting
- open your index.html file inside github.com
- click on raw button above the html code
- change in the url `raw.githubusercontent.com` with `raw.githack.com`
and it will give you a usable URL for sharing your documentation. 

2. #### Share the URL:
    The URL provided by RawGitHack can now be used to access the documentation from any 
    browser.

### Summary of Changes/Clarifications:
- `sphinx-apidoc -o docs .` generates reStructuredText files for your Python modules.
- You should add the `modules` directive in the `index.rst` to include the generated module documentation.
- Make sure to update your `sys.path` in `conf.py` so that Sphinx can locate your project.
- Set a clean and modern theme like `sphinx_rtd_theme` in `conf.py`.
- Building the HTML using the make command (`make html` on Unix, `.\make.bat html` on Windows).
- For quick online hosting, you can use RawGitHack.

This should help you generate and share Sphinx documentation smoothly!

### Steps to Update the Sphinx HTML Documentation:
1. #### Regenerate Documentation Stubs (If Needed):
    If you’ve added new modules or modified existing ones, run the following command 
    from your project root to update the `.rst` files:
    ```
   > sphinx-apidoc -o docs .
   ```
2. #### Build the Updated HTML:
    Navigate to the `docs` folder and run the Sphinx build command again to regenerate the HTML files:
    ```
    > cd docs
    > .\make.bat html  # On Windows
    # or
    > make html        # On Unix/macOS
    ```
    This will overwrite the existing HTML files in the `docs/_build/html` directory with the latest version.
    If you moved your html file you can replace it with the new one build in `docs/_build/html`.
3. #### Deploy Update HTML:
   If you're hosting the documentation online (e.g., using [RawGitHack](#use-rawgithack-for-hosting) or GitHub Pages), you’ll need to commit and push the updated files to your repository:
   - Make sure the updated HTML files are in the appropriate location (e.g., `docs/_build/html`).

### Command Summary of Update the Sphinx HTML Documentation:
```
# From project root, regenerate the .rst files (optional if no new modules were added)
> sphinx-apidoc -o docs .

# Navigate to the docs folder
> cd docs

# Build the updated HTML files
> .\make.bat html    # For Windows
# or
> make html          # For Unix/macOS
```

   
