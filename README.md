 ##########################################################################
 
   Copyright (C) 2021-2022 stinger81

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
   stinger81 - GitHub
 
 ##########################################################################
# Desktop CLean Up Tool
Tool Designed to clean up desktop and store it all in a folder 

Designed and tested on windows and WSL*

*WSL mounts back to main C drive. Bash script developed to be ran from WSL or linux.

Can be should work on standard linux and MacOS however it is not tested

When entering directory regardless of OS use "\\\\" to separate 

## Ignoring Specific Directories, Files and Extensions
* The same principle is used as in .gitignore
* "/" at the end of a line dictates a directory to ignore
* "*" at the beginning of a line will dictate a file extension to ignore
* "insertFileNameHere.FileExtension" will ignore a specific file
* "#" will suppress a line and it will not be read by the program
