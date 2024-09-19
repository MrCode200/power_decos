## How to Use Sphinx generating html

### First time commands:
1. ```cd docs```
2. ```sphinx-quickstart```
3. ```cd ..```
4. ```sphinx-apidoc -o docs .```

5. Go To `index.rst` inside of docs folder and insert `module`:
    ```
   Power Decos documentation
    =========================

    .. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules # insert modules here
   
6. Inside the `config.py` Add this line of code above `project = 'project name'`:
    ```
   import os, sys

    sys.path.insert(0, os.path.abspath(".."))
   
7. Change `extensions` to:
    ```
   extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]
   
6. Change theme in `html_theme` and `html_static_path` to:
    ```
    html_theme = 'sphinx_rtd_theme'
    html_static_path = ['_static']```
   
### Commands for generating file
1. `cd docs`
2. `.\make.bat html` type `.\make.bat` to see all available other types
3. Now you can move the html file to every location
4. You can run `index.html` in your browser

### Host online

1. Visit https://raw.githack.com/
2. In github open your `index.html` and copy with the three dots `...` the `Copy Permalink`
3. Insert permalink inside of raw.githack 
4. Congrats you are finished. URL can be used by every one
