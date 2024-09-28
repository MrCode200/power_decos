@ECHO OFF
:: sphinx-quickstart command
sphinx-quickstart || (echo !RED!BOLD FAILED: sphinx-quickstart did not run !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [1/5]: sphinx-quickstart completed !RESET!

:: Move up one directory
cd ..

:: sphinx-apidoc command
sphinx-apidoc -o docs . || (echo !RED!BOLD FAILED: Couldn't generate rst files !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [2/5]: Created rst files !RESET!

:: Change to docs directory
cd docs

:: Insert text into index.rst
sed -i '13a modules' index.rst || (echo !RED!BOLD FAILED: Couldn't modify index.rst !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [3/5]: Modified index.rst !RESET!

:: Modify extensions in config.py
sed -i '21s/.*/extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]/' config.py || (echo !RED!BOLD FAILED: Couldn't modify config.py !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [4/5]: Modified extensions in config.py !RESET!

:: Modify theme in config.py
sed -i '23s/.*/html_theme = "sphinx_rtd_theme"/' config.py || (echo !RED!BOLD FAILED: Couldn't modify theme in config.py !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [5/5]: Modified theme in config.py !RESET!