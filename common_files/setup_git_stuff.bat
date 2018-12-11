PUSHD %~dp0

if exist "%PROJECT%" goto :ProjectExists
git clone %HOST%:%ORGANIZATION%/%PROJECT%
PUSHD %PROJECT%
git checkout master
git pull

PUSHD src
mkdir %PROJECT%.Mapper

PUSHD %PROJECT%.Mapper
git submodule add %HOST%:%ORGANIZATION%/shared

PUSHD shared
git checkout master
git pull
POPD

POPD
POPD
POPD
POPD
:ProjectExists
exit /b