import os
from os.path import isfile, isdir, join
import subprocess
from shutil import copy

from GitRepo import GitRepo
from ErrorLog import ErrorLog


main_dir_path = "C:\\Starcounter"
common_file_path = os.getcwd() + "\\common_files"


def SetupProject(git_repo):
    error_log = ErrorLog()
    setup_bat_file_path = join(common_file_path, 'setup_git_stuff.bat')
    dst_file_path = join(main_dir_path, 'setup_git_stuff.bat')
    if not os.path.exists(setup_bat_file_path):
        error_log.LogError("Setup Git Stuff file template not found")
        return False
    try:
        with open(setup_bat_file_path) as setup_file:
            dst_file = open(dst_file_path, 'w+')
            for line in setup_file:
                temp_line = line.replace('%HOST%', git_repo.host)
                temp_line = temp_line.replace('%ORGANIZATION%', git_repo.organization)
                temp_line = temp_line.replace('%PROJECT%', git_repo.project)
                dst_file.write(temp_line)
            dst_file.close()
    except OSError:
        error_log.LogError("Unable to generate bat file for git")
        return False
    try:
        subprocess.call([dst_file_path])
    except:
        error_log.LogError("Git setup bat file execution failed for " + git_repo.project)
        return False
    os.remove(dst_file_path)
    return True

def FixStupidSolutionFile(proj_name):
    error_log = ErrorLog()
    temp_sln_file_path = join(main_dir_path, proj_name, proj_name + "_temp.sln")
    sln_file_path = join(main_dir_path, proj_name, proj_name + ".sln")

    os.rename(sln_file_path, temp_sln_file_path)

    try:
        with open(temp_sln_file_path) as sln_file:
            output_file = open(sln_file_path, 'w+')
            for line in sln_file:
                if line.find('"src", "src",') != -1:
                    sln_file.readline()
                elif line.find('GlobalSection(NestedProjects) = preSolution') != -1:
                    sln_file.readline()
                    sln_file.readline()
                else:
                    output_file.write(line)
            output_file.close()
    except OSError:
        error_log.LogError("Unable to fix " + proj_name + " solution file")
        return
    os.remove(temp_sln_file_path)

def RemoveFile(path):
    error_log = ErrorLog()
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            error_log.LogError("Unable to delete " + path)


def RemoveNugetExe(path):
    error_log = ErrorLog()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower() == "nuget.exe":
                os.remove(join(root, file))
                if not os.listdir(root):
                    os.removedirs(root)
                return
    error_log.LogError("Could not find nuget.exe in dir " + path)


def MoveInMappingFiles(proj_name):
    error_log = ErrorLog()
    mapping_path = join(main_dir_path, proj_name + '.Mapper', 'cpp')
    dst_path = join(main_dir_path, proj_name, 'src', proj_name + '.Mapper')
    for file_name in os.listdir(join(mapping_path)):
        if file_name.find('.map.cpp') == -1:
            try:
                copy(join(mapping_path, file_name), dst_path)
            except OSError:
                error_log.LogError("Failed to move mapper file: " + join(mapping_path, file_name))

def AddCustomFile(src_dir, file_name, replace_value, dst_dir):
    error_log = ErrorLog()
    orig_file_path = join(src_dir, file_name)
    if not os.path.exists(orig_file_path):
        error_log.LogError("Common file template not found")
        return
    dst_file_path = join(dst_dir, file_name)
    if file_name.find('AppName') != -1:
        dst_file_path = join(dst_dir, file_name.replace('AppName', replace_value))
    try:
        with open(orig_file_path) as orig_file:
            dst_file = open(dst_file_path, 'w+')
            dst_file.write(orig_file.read().replace('%REPLACE%', replace_value))
            dst_file.close()
    except OSError:
        error_log.LogError("Unable to create custom file " + file_name + " with replace value " + replace_value)

def AddMainDirCommonFile(dst_path):
    error_log = ErrorLog()
    src_dir_path = join(common_file_path, 'main_dir')
    dir_contents = os.listdir(src_dir_path)
    for f in dir_contents:
        src_file_path = join(src_dir_path, f)
        if isfile(src_file_path):
            try:
                copy(src_file_path, dst_path)
            except OSError:
                error_log.LogError("Unable to copy file " + f + " to " + dst_path)
        elif not isdir(src_file_path):
            error_log.LogError("Unable to copy file " + f + " to " + dst_path)


def AddMainDirCustomFiles(proj_name):
    src_dir = join(common_file_path, 'main_dir', 'replaceable')
    for file_name in os.listdir(src_dir):
        if isfile(join(src_dir, file_name)):
            AddCustomFile(src_dir, file_name, proj_name, join(main_dir_path, proj_name))

def AddMapperProjToSolution(proj_name):
    bat_file_path = join(main_dir_path, proj_name, 'add_project.bat')
    AddCustomFile(common_file_path, 'add_project.bat', proj_name, join(main_dir_path, proj_name))
    try:
        subprocess.call([bat_file_path])
    except:
        error_log.LogError("Unable to fix sln for " + proj_name + " Project")
    FixStupidSolutionFile(proj_name)
    os.remove(bat_file_path)

def UpdateMgenJson(proj_name):
    mgen_file_path = join(main_dir_path, proj_name, "src", proj_name + ".Mapper", 'mgen.json')
    temp_file_path = join(main_dir_path, proj_name, "src", proj_name + ".Mapper", 'mgen_temp.json')

    os.rename(mgen_file_path, temp_file_path)

    try:
        with open(temp_file_path) as mgen_file:
            output_file = open(mgen_file_path, 'w+')
            for line in mgen_file:
                if line.find('..\\\shared') != -1:
                    output_file.write(line.replace('..\\\shared', 'shared'))
                elif line.find('appAssembly') != -1:
                    output_file.write('  "appAssembly": "..\\\$app$\\\\bin\\\$config$\\\$app$.exe",\n')
                elif line.find('mapperOutput') != -1:
                    output_file.write('  "mapperOutput": "..\\\$app$\\\\bin\\\$config$\\\$app$.map.cpp",\n')
                else:
                    output_file.write(line)
            output_file.close()
    except OSError:
        error_log.LogError("Unable to fix " + proj_name + " mgen file")
        return
    os.remove(temp_file_path)

# MAIN
error_log = ErrorLog()
subfolders = [f.path for f in os.scandir(main_dir_path) if f.is_dir()]
for dir in subfolders:
    if dir.find(".Mapper") != -1 and dir.find("Blending") == -1:
        proj_name = dir.split('\\')[-1].split('.')[0]
        git_repo = GitRepo()
        git_repo.SetProject(proj_name)
        if SetupProject(git_repo):
            # Remove unneccessary dirs
            RemoveFile(join(main_dir_path, proj_name, 'Rebracer.xml'))
            RemoveNugetExe(join(main_dir_path, proj_name))
            # Add new dirs not added by setup bat
            try:
                os.mkdir(join(main_dir_path, proj_name,'%STAR_NUGET%'))
            except OSError:
                error_log.LogError("%STAR_NUGET% folder already exists for " + proj_name + " Project")
            # Setup src/Mapper folder by copying relevant mapping files from mapping repo
            MoveInMappingFiles(proj_name)
            # Add Mapper Specific csproj file
            AddCustomFile(join(common_file_path, 'mapper_dir'), 'AppName.Mapper.csproj', proj_name, join(main_dir_path, proj_name, 'src', proj_name + '.Mapper'))
            AddCustomFile(common_file_path, 'commit_stuff_to_git.bat', proj_name, main_dir_path)
            # Update mgen.json file
            UpdateMgenJson(proj_name)
            # Add mapper proj to main project
            AddMapperProjToSolution(proj_name)
            # Add constant files to main dir
            AddMainDirCommonFile(join(main_dir_path, proj_name))
            # Add custom files to main dir
            AddMainDirCustomFiles(proj_name)
            # execute a build to see if it works
            try:
                result = subprocess.call([join(main_dir_path, proj_name, 'build.bat')])
            except:
                error_log.LogError("Unable to build " + proj_name + " Project")
            # if it works, then check stuff in
            if result == 0:
                add_project_path = join(main_dir_path, "commit_stuff_to_git.bat")
                subprocess.call([add_project_path])
                os.remove(add_project_path)
            else:
                error_log.LogError("Build Error for " + proj_name + " Project")


            # we should be done then

