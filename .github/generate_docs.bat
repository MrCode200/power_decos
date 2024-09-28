@echo off
cd %~dp0 || (echo Failed to get current path. Exiting... & exit /b 1)
echo Successfully moved to script path: %currentPath%

echo %cd%
cd ..\docs || (echo Failed to change directory to docs. Exiting... & exit /b 1)
echo Changed directory to docs.

call .\make.bat html || (echo Failed to run make.bat. Exiting... & exit /b 1)
echo Documentation generated successfully.

robocopy "_build\html" "html" /E /MOVE /R:3 /W:5 /V
echo HTML files moved successfully(? - throws error dont know why when using || exit /b 1).

IF EXIST "_build\html" rmdir /S /Q "_build\html" || (echo Failed to delete html folder inside _build. Exiting.. & exit/b 1)
echo Deleted html files inside _build

git commit -a -m "Updated documentation" || (echo Failed to commit changes. Exiting... & exit /b 1)
echo Changes committed successfully.

git push || (echo Failed to push changes. Exiting... & exit /b 1)
echo Changes pushed successfully.

@echo on
git status || (echo Failed to retrieve Git status. Exiting... & exit /b 1)