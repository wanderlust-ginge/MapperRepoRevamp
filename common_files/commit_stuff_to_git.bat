PUSHD %~dp0
PUSHD %REPLACE%

git add .
git commit -m "Project/Mapper merge"
POPD
POPD

:ProjectExists
exit /b