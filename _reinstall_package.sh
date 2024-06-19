#!/bin/bash

get_conda_env_name()
{
        conda info |awk '/active environment/{print $4}'
}


# Function to reinstall package
reinstall_package_python() { 
  # validate we have  a path   
  if [ -z $1 ]; then
    echo "Please provide a path to the package directory"
    return
  fi
  local cdir=$(pwd)
  # Navigate to the provided directory
  cd $1
  #validate we have a pyproject.toml file
  if [ ! -f pyproject.toml ]; then
    echo "The provided directory does not contain a pyproject.toml file"
    cd $cdir
    return
  fi
  # Extract the package name from pyproject.toml
  package_name=$(cat pyproject.toml | grep -oP '(?<=name = ").*(?=")')

  # Find the .whl file in the dist directory
  dist_path=$(realpath $(du -a dist | grep whl | awk '{print $2}'))
  #current_conda_env=$(conda info |awk '/active environment/{print $4}')
  current_conda_env=$(get_conda_env_name)

  #if the package_name and conda env name is not the same
  if [ "$package_name" == "$current_conda_env" ]; then
    echo "The package name $package_name is the same as the current conda environment $current_conda_env"
    echo "We will not reinstall the package - ASSUMING that was ran by mistake in the dev env of the package."
    cd $cdir
    return
  fi
  cd $cdir

  # Uninstall the current package
  pip uninstall $package_name -y

  # Install the package using the .whl file
  pip install $dist_path
}



# Call the function with the first script argument
reinstall_package_python $1

