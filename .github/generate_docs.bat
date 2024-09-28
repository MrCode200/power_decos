@echo off
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

SETLOCAL EnableDelayedExpansion

:: Set ANSI colors
SET GREEN=!ESC![1;32m
SET RED=!ESC![1;31m
SET RESET=!ESC![0m

pip install sphinx sphinx_rtd_theme

echo %GREEN% SUCCESSFULL [0/11]: Installed libaries and dependencies. %RESET%

cd %~dp0 || (echo %RED% FAILED: Couldn't get current path. Exiting... %RESET% & exit /b 1)
echo %GREEN% SUCCESSFULL [1/11]: Moved to script path: %currentPath% %RESET%

echo %cd%
cd ..\docs || (echo %RED% FAILED: Couldn't change directory to docs. Exiting... %RESET% & exit /b 1)
echo %GREEN% SUCCESSFULL [2/11]: Changed directory to docs. %RESET%

SET /P USER_INPUT="Have you setup the sphinx (One time action)? (y/n): "

IF /I "%USER_INPUT%"=="n" (
    call ..\.github\init_docs.bat || (echo %RED% FAILED: Initialization of sphinx documentation failed %RESET% & exit /b 1)
    echo %GREEN% SUCCESSFULL [3/11]: Successfully initilized sphinx documentation. %RESET%
    exit /b 1
)

SET /P USER_INPUT="Have you added new files(modules/packages/testsfiles) - (NOTE: Not edited)? (y/n): "

IF /I "%USER_INPUT%"=="n" (
    cd ..

    del modules.rst
    del power_decos.rst
    del tests.rst

    sphinx-apidoc -o docs . || (echo %RED% FAILED: Couldn't run `sphinx-apidoc -o docs .` -> no rst files generated %RESET% & exit /b 1)
    echo %GREEN% SUCCESSFULL [4/11]: Created rst files %RESET%

    cd docs
)

call .\make.bat html || (echo %RED% FAILED: Couldn't run make.bat. Exiting... %RESET% & exit /b 1)
echo %GREEN% SUCCESSFULL [5/11]: Documentation generated successfully. %RESET%

robocopy "_build\html" "html" /E /MOVE /R:3 /W:5 /V
echo %GREEN% SUCCESSFULL [6/11]: HTML files moved successfully. %RESET%

IF EXIST "_build\html" rmdir /S /Q "_build\html" || (echo %RED% FAILED: Couldn't delete html folder inside _build. Exiting... %RESET% & exit /b 1)
echo %GREEN% SUCCESSFULL [7/11]: Deleted html files inside _build. %RESET%

git add ./html/ || (echo %RED% FAILED: Couldn't add html directory inside docs. Exiting... %RESET% & exit /b 1)
echo %GREEN% SUCCESSFULL [8/11]: Tracked html file (git). %RESET%

SET /P USER_INPUT="Do you want to commit and push html directory to github? (y/n): "

IF /I "%USER_INPUT%"=="y" (
    git commit html -m "Updated documentation" || (echo %RED% FAILED: Couldn't commit changes. Exiting... %RESET% & exit /b 1)
    echo %GREEN% SUCCESSFULL [9/11]: Changes inside html directory committed successfully. %RESET%

    git push || (echo %RED% FAILED: Couldn't push changes. Exiting... %RESET% & exit /b 1)
    echo %GREEN% SUCCESSFULL [10/11]: Changes pushed successfully. %RESET%

    @echo on
    git status || (echo %RED% FAILED: Couldn't retrieve Git status. Exiting... %RESET% & exit /b 1)

    echo %GREEN% SUCCESSFULL [11/11]: Process Finished. Exiting... %RESET%
) ELSE (
    echo %GREEN% SUCCESSFULL [11/11]: Process Finished. Exiting... %RESET%
)
