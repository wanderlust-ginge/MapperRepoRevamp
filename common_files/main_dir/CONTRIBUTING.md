# Developer instructions

## Prerequisites

* Install [.NET Core SDK version 2.1.400 or later](https://dotnet.microsoft.com/download)
* Install the latest global .NET Core Cake tool by running `dotnet tool install -g Cake.Tool` which is only needed for using the CLI scripts.
* Have the NuGet packages `M.nupkg` and `MGen.nupkg` on local feed. This can be done by placing them in [%STAR_NUGET%](./%25STAR_NUGET%25) folder or by setting the environment variable to the folder where they are located, example: `set STAR_NUGET="C:\FolderContainingNuGetPackages"`
  * `M.nupkg` may be built from the [DoctorM](https://github.com/Starcounter/DoctorM) git repository while `MGen.nupkg` may be built from [MGen](https://github.com/Starcounter/MGen).
* [Visual Studio 2017](https://www.visualstudio.com/downloads/) --version 15.8.2 or higher.
  * Make sure .NET Framework 4.7.2 is installed in VS 2017.  If not, run the VS Installer, select "Modify" and then in "Individual Components", select that version and continue on.
* [DebugView](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview) which is used to debug the mapper.

## How to build and run

### Build and run using CLI

1. Clone this repo to your local machine
2. Build the solution by executing `build.bat` in Windows or `./build.bat` in Git Bash
3. Run it by executing `run.bat` in Windows or `./run.bat` in Git Bash

There is also a `package.bat` script which creates a StarPack of the application.

### Build and run using Visual Studio

1. Clone this repo to your local machine
2. Open the `.sln` file in Visual Studio
3. Build and run it using Debug in Visual Studio (**Debug** > **Start debugging** or <kbd>F5</kbd>). Note that you have to start `M.exe` yourself by doing this.

### Using Debug View
We are currently using Microsoft's DebugView to chase down errors with the mappers.
* After downloading DebugView, run as an administrator.
* The first window to pop up should be the DebugView Filter. If not, you can find it under Edit->Filter/Highlight
* add `sc_` to `Include` filters
* make sure it's running in the background. If the app crashes due to mapping, something *should* pop up.  the message/messages you get combined with a brief description of the steps you took prior to the crash will hopefully help identify what caused the crash.

## Contributing code

To contribute code to this repository, follow the instructions in the [guidelines](https://starcounter.gitbooks.io/guidelines/content/contributing-code.html).

## How to release a package

To release the app to the warehouse, follow the instructions in the [guidelines](https://starcounter.gitbooks.io/guidelines/content/releasing-to-warehouse.html).