#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Adapted from the original script by:
#   - J. Jahan (jjahan@uh.edu) 
#   - D. Friedenberg (dfriede1@tamu.edu) 
################################################################################################

import sys as sys
import os as os
import subprocess as sub
import yaml as yaml
import json as json
from openapi_core import Spec
from openapi_core import validate_request
from openapi_core import unmarshal_request
from openapi_core.testing import MockRequest

#=========================#
# OPENAPI INPUT VALIDATOR #
#=========================#
def OpenAPI_validator(specs_file_path, input_file_path, verbose=False, print_valid=True):    

    api_path = os.path.abspath(os.path.dirname(__file__))
    out_path = api_path[:-3] + "output/"
    
    # Ensuring input files are found at specified locations
    #-------------------------------------------------------
    #Specs file
    if not os.path.exists(specs_file_path):
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"[OpenAPI_input_validator]> File '" + specs_file_path + "' not found."}, outfile, default_flow_style=False)
        print("[OpenAPI_input_validator]> File '" + specs_file_path + "' not found \n\nOPERATION ABORTED")
        sys.exit(3)
    
    #YAML file
    if not os.path.exists(input_file_path):
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"[OpenAPI_input_validator]> File '" + input_file_path + "' not found."}, outfile, default_flow_style=False)
        print("[OpenAPI_input_validator]> File '" + input_file_path + "' not found \n\nOPERATION ABORTED")
        sys.exit(3)
    
    # Reading OpenAPI specifications
    #--------------------------------
    with open(specs_file_path, 'r') as spec_file:
        openapi_specs = Spec.from_file(spec_file)
    
    #~Extract name of input file
    input_file = input_file_path[input_file_path.rfind('/')+1:]
    
    #~Find corresponding path in specifications
    input_spec_path = ''
    for path in openapi_specs["paths"].keys():
        if input_file in path:
            input_spec_path = path

    #~Stop program if no match found
    if input_spec_path == '':
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":500, "message":"[OpenAPI_input_validator]> No path found in specifications matching '" + input_file_path + "'."}, outfile, default_flow_style=False)
        print("[OpenAPI_input_validator]> No path found in specifications matching '" + input_file_path + "' \n\nOPERATION ABORTED")
        sys.exit(3)
    
    # Reading input file
    #--------------------
    with open(input_file_path, 'r') as input_file:
        data = yaml.safe_load(input_file)
    
    # Define request
    #----------------
    #For input files
    if 'input/' in input_file_path:
        operation = "PUT"
    
    #For output files    
    if 'output/' in input_file_path:
        operation = "GET"
    
    #Define the request object
    request = MockRequest(
        host_url='/',
        method=operation,
        path=input_spec_path,
        data=json.dumps(data)
    )
    
    #To store error messages if there are
    errors = "" 
    
    # Validate the request
    #----------------------
    try: #use 'try' to not interrupt the program in case 'validate_request()' finds errors
        #~Validate parameters that are properly defined
        valid_request = unmarshal_request(spec=openapi_specs, request=request)
    
    # Raise error message if problem in validation
    #----------------------------------------------
    except Exception as e:
        for error in e.__cause__.schema_errors:
            #~Skip "None for not nullable" error as it always come double with another error, for when no value is given for a property
            if error.message != "None for not nullable":
                #~For errors associated with a given defined property
                if len(error.relative_path) != 0:
                    errors += "\n   ['"+ error.relative_path[0] +"'] -> "+ error.message
                else:
                    errors += "\n  -> "+ error.message
    
    # Print message for validation 
    #------------------------------
    if errors != "":
        #~Failed validation
        print("Failed to validate "+ input_file_path +" with module specifications.")
        if verbose:
            errors = "Raised errors:" + errors
            print(errors)
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"Failed to validate "+ input_file_path +" with module specifications.\n"+ errors}, outfile, default_flow_style=False)        
        sys.exit(1)
    else: 
        if verbose:
            #~Successful validation
            print("Successful validation of %s"%(input_file_path))
    
    
    # Create valid input file (if required)
    #---------------------------------------
    if print_valid:
        #~Define path of new valid input file
        input_path = input_file_path[:input_file_path.rfind('/')+1]
    
        #~Define name of new valid input file
        valid_input_name = 'valid_'+input_file_path[input_file_path.rfind('/')+1:]
    
        #~Complete path + name of new valid input file
        valid_input_file = os.path.join(input_path, valid_input_name)
    
        #~Create new valid input file
        with open(valid_input_file, "w") as valid_input:
            yaml.safe_dump(valid_request.body, valid_input)
        
    # Returning name of (validated) input file
    #------------------------------------------
        return valid_input_name
    #If not valid file required
    else:
        return input_file_path


#======#
# MAIN #
#======#
if __name__ == '__main__':
    # Inputs 
    #--------    
    if len(sys.argv) == 3:
        #~Affect arguments 
        specs_file_path = sys.argv[1] 
        input_file_path = sys.argv[2]
    if len(sys.argv) < 3:
        #~Exit with error message if missing arguments
        with open(os.path.join(out_path, "status.yaml"), 'w') as outfile:
            yaml.dump({"code":400, "message":"[OpenAPI-Specifications_validator.py]> Missing arguments: should be 2 (specifications file + input file to validate)."}, outfile, default_flow_style=False)
        print("[OpenAPI-Specifications_validator.py]> Missing arguments: should be 2 (specifications file + input file to validate)")
        sys.exit(2)
    
    # Validation
    #------------
    OpenAPI_input_validator(specs_file_path, input_file_path, verbose=True)

