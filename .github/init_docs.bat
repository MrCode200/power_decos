@ECHO OFF
:: sphinx-quickstart command
sphinx-quickstart || (echo !RED!BOLD FAILED: sphinx-quickstart did not run !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [1/7]: sphinx-quickstart completed !RESET!

:: Move up one directory
cd ..

:: sphinx-apidoc command
sphinx-apidoc -o docs . || (echo !RED!BOLD FAILED: Couldn't generate rst files !RESET! & exit /b 1)
echo !GREEN!BOLD SUCCESSFUL [2/7]: Created rst files !RESET!

:: Change to docs directory
cd docs

:: Insert text into index.rst
:: Step 1: Delete lines 8 to 12 from index.rst
powershell -Command ^
    "$content = Get-Content 'index.rst';" ^
    "$newContent = $content[0..7] + $content[13..($content.Count - 1)];" ^
    "$newContent | Set-Content 'index.rst';"

:: Check ERRORLEVEL after the PowerShell command
if ERRORLEVEL 1 (
    echo !RED! FAILED: Couldn't delete lines in index.rst !RESET!
    exit /b 1
)

echo !GREEN! SUCCESSFUL [3/7]: Deleted lines in index.rst !RESET!

:: Insert 'modules' into index.rst
powershell -Command ^
    "$content = Get-Content 'index.rst';" ^
    "$newContent = $content[0..11] + '  modules' + $content[12..($content.Count - 1)];" ^
    "$newContent | Set-Content 'index.rst';"

:: Check ERRORLEVEL after the PowerShell command
if ERRORLEVEL 1 (
    echo !RED! FAILED: Couldn't insert 'modules' into index.rst !RESET!
    exit /b 1
)

echo !GREEN! SUCCESSFUL [4/7]: Inserted lines in index.rst !RESET!

:: Step 5: Insert lines into conf.py at line 8
powershell -Command ^
    "$content = Get-Content 'conf.py';" ^
    "$newContent = $content[0..7] + @('import os, sys', 'sys.path.insert(0, os.path.abspath(''..''))') + $content[8..($content.Count - 1)];" ^
    "$newContent | Set-Content 'conf.py';"

:: Check ERRORLEVEL after the PowerShell command
if ERRORLEVEL 1 (
    echo !RED! FAILED: Couldn't insert lines into conf.py !RESET!
    exit /b 1
)

echo !GREEN! SUCCESSFUL [5/7]: Inserted lines into conf.py !RESET!

:: Modify extensions in conf.py
powershell -Command ^
    "(Get-Content 'conf.py') | ForEach-Object { if ($_ -match '^extensions =') { 'extensions = [\"sphinx.ext.todo\", \"sphinx.ext.viewcode\", \"sphinx.ext.autodoc\"]' } else { $_ } } | Set-Content 'conf.py'" || (echo !RED! FAILED: Couldn't modify extensions in config.py !RESET! & exit /b 1)

echo !GREEN! SUCCESSFUL [6/7]: Modified extensions in config.py !RESET!

:: Modify theme in config.py
powershell -Command ^
    "(Get-Content 'conf.py') | ForEach-Object { if ($_ -match '^html_theme =') { 'html_theme = \"sphinx_rtd_theme\"' } else { $_ } } | Set-Content 'conf.py'" || (echo !RED! FAILED: Couldn't modify theme in config.py !RESET! & exit /b 1)

echo !GREEN! SUCCESSFUL [7/7]: Modified theme in config.py !RESET!
