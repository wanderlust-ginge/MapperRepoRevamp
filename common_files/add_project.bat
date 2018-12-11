PUSHD %~dp0

dotnet sln %REPLACE%.sln add src/%REPLACE%.Mapper/%REPLACE%.Mapper.csproj
POPD

exit /b