#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------
#version: 1.0.0
#-----------------------------------------------------------------------------------------------
# |Gaussian Process Generator|
# ----------------
# Main script called to run the module.
# Relies on functions defined in:
# - src/GaussianProcessCrossSectionGenerator.py
# - src/GaussianProcessCrossSectionTabulator.py
# - src/GaussianProcessCrossSectionPlotter.py
# and specifications in:
# - api/OpenAPI_Specifications.yaml
# - api/OpenAPI_Specifications_validator.py
# to validate inputs.
#
# Inputs are the YAML files containing parameters, taken as arguments when calling the script.
# Ex.:
# $> python src/main.py input/config.yaml
################################################################################################

import sys as sys
import os as os
import yaml as yaml
import subprocess as sub

# Determine current path to define all other paths relative to it
pwd = os.path.abspath(os.path.dirname(__file__))
home_path = pwd[:pwd.rindex('/') + 1]

api_path = os.path.join(home_path, 'api/')
inp_path = os.path.join(home_path, 'input/')
out_path = os.path.join(home_path, 'output/')
src_path = os.path.join(home_path, 'src/')

# Add path to the libraries with converting functions
from GaussianProcessCrossSectionGenerator import *
from GaussianProcessCrossSectionTabulator import *
from GaussianProcessCrossSectionPlotter import *
from PolynomialCrossSectionGenerator import *
sys.path.append(api_path)
from OpenAPI_Specifications_validator import *

#--------#
# INPUTS #
#--------#

#Affecting the list of arguments given in the command line
args = sys.argv[1:]

# Ensuring input files are found
#--------------------------------

#Loop over files given as inputs
for arg in args:
     #If absent file...
    if not os.path.exists(arg):
        #...create 'status.yaml' with error code + message and stop module execution
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"[main.py]> File '" + arg + "' not found."}, outfile, default_flow_style=False)
        sys.exit("[main.py]> File '" + arg + "' not found \n\nOPERATION ABORTED")

# Ensuring inputs are valid
#---------------------------

#Define path to module specifications
specifications = os.path.join(api_path, 'OpenAPI_Specifications.yaml')

#Extract specifications from file
with open(specifications, 'r') as spec_file:
    openapi_specs = Spec.from_file(spec_file)

#Dictionnary to store information on input files from specifications
spec_input_files = {}

#Collecting information on input files in specifications
for path in openapi_specs["paths"].keys():
    #Check if 'path' correspond to an input file
    if "input" in path:
        #Add it to the spec_input_files{} dict. and indicate if required + add call marker
        spec_input_files[path[1:]] = {"required": openapi_specs["paths"][path]["put"]["requestBody"]["required"], "called": False, "copied": False}

#Looping over input files
for arg in args:
    #Validate input file against module's OpenAPI specifications 
    valid_input = OpenAPI_validator(specifications, arg, verbose=True)
    #Loop over input files from specs
    for input_file in spec_input_files.keys():
        #Mark file as called if positive
        if input_file in arg:
            spec_input_files[input_file]["called"] = True
    #Assign name of new validated + unmarshaled input files
    if "config.yaml" in arg: 
        input_user = valid_input

#Loop over input files info from specs
for input_file in spec_input_files.keys():
    #If required file not called with the script...
    if spec_input_files[input_file]["required"] == True and spec_input_files[input_file]["called"] == False:
        #...create 'status.yaml' with error code + message and stop module execution
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"[main.py]> Missing required file: " + input_file}, outfile, default_flow_style=False)
        sys.exit("[main.py]> Missing required file: " + input_file + "\n\nOPERATION ABORTED")
        
#--------------#
# INPUT PARSER #
#--------------#
#------------------#
# RUNNING THE CODE #
#------------------#

#Define command line to execute 
CrossSection = GaussianProcessCrossSection()
tabulate_gp_cross_section(CrossSection, out_path)
plot_gp_cross_section(out_path)
    
#----------------#
# OUTPUT PLOTTER #
#----------------#

        
#----------------------------------------------#
# WRITING STATUS FILE FOR SUCCESSFUL OPERATION #
#----------------------------------------------#
with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
    yaml.dump({"code":200, "message":"Succcessful module execution"}, outfile, default_flow_style=False)
    
print("")