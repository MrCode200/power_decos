@ECHO OFF
:: sphinx-quickstart command
sphinx-quickstart || (echo !RED!BOLD FAILED: sphinx-quickstart did not run !RESET! & exit /b 1)
echo !GREEN! SUCCESSFUL [1/5]: sphinx-quickstart completed !RESET!

:: Move up one directory
cd ..

:: sphinx-apidoc command
sphinx-apidoc -o docs . || (echo !RED!BOLD FAILED: Couldn't generate rst files !RESET! & exit /b 1)
echo !GREEN! SUCCESSFUL [2/5]: Created rst files !RESET!

:: Change to docs directory
cd docs

:: Insert text into index.rst
powershell -Command "(Get-Content 'index.rst')[0..11] + 'modules' + (Get-Content 'index.rst')[12..$null] | Set-Content 'index.rst'" || (echo !RED!BOLD FAILED: Couldn't modify index.rst !RESET! & exit /b 1)
echo !GREEN! SUCCESSFUL [3/5]: Modified index.rst !RESET!

:: Modify extensions in config.py
powershell -Command "(Get-Content 'conf.py') | ForEach-Object { if ($_ -match '^extensions =') { 'extensions = [\"sphinx.ext.todo\", \"sphinx.ext.viewcode\", \"sphinx.ext.autodoc\"]' } else { $_ } } | Set-Content 'config.py'" || (echo !RED!BOLD FAILED: Couldn't modify config.py !RESET! & exit /b 1)
echo !GREEN! SUCCESSFUL [4/5]: Modified extensions in config.py !RESET!

:: Modify theme in config.py
powershell -Command "(Get-Content 'config.py') | ForEach-Object { if ($_ -match '^html_theme =') { 'html_theme = \"sphinx_rtd_theme\"' } else { $_ } } | Set-Content 'config.py'" || (echo !RED!BOLD FAILED: Couldn't modify theme in config.py !RESET! & exit /b 1)
echo !GREEN! SUCCESSFUL [5/5]: Modified theme in config.py !RESET!
