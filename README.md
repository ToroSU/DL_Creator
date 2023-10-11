![image](https://github.com/ToroSU/DL_Creator/blob/main/LOGO1.PNG)

# Introduction
Create driver list for Customer History:  

# Development  Environment
Main = Python, version:3.10.0  
GUI = PyQt5, version:5.15.6  
GUI design = Qt Designer
Excel = openpyxl

# Version History
Dev 1.5.1:  
Fix: Directly running the Tool can cause an issue where the config file is not saved (this results in the tool having no config.ini to read from).  
Add: After pressing "Run", a message indicating that the config file has been successfully saved will be displayed.  

Dev 1.5.0:  
Add Feature: Add create "Release Note" sheet content function.

Dev 1.4.1:  
Fix: Fix the inf name output error when the intermediate version is modified (Variable name wrong.)  

Dev 1.4:  
Add Feature: Add compression function  
Fix : Add check list for RPL-Platform  

Dev 1.3.2:  
Add Feature: Check box is automatically disabled and set uncheck for foolproof use.  

Dev 1.3.1:   
Add Feature: Buttons are disabled when not usable.

# Planned Updates (in order of priority):  
  
1. Fix most of the known bugs and release v1.6 stable version as the completion of the old SOW. Updates can be stopped if not necessary.  
2. Follow the new Driver list SOW (after SOW 2.4) and release as version 2.0.  
3. Allow the inf_check_list in DLC_info_catch to be directly edited from an external config file, improving convenience.  
4. Investigate the possibility of dynamic resolution adjustment (currently, the Tool appears too large at 150% resolution, making the "Run" button inaccessible).  
5. Redesign the GUI layout.  
6. Update the Wlan/BT fields to dynamic mode (display corresponding fields only after the user selects a manufacturer).  
