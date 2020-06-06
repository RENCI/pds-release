# pds-release
Repo for facilitating coordinated release of multiple pds repos


# how to add your repo in a release

## add submodule
Add your repo as a submodule under the `module` dir

Your repo should have a Dockerfile

Your repo should also have a tag x.y.z

If the commit of your repo is not tagged then the hash is going to be used as the tag

## add yml

Add a yml file under the `plugin` dir

how to write the yml file

see example under plugin/pds.yml

the image name should be the same as the submodule dir name

the tag should be from envrionment variable <submodule>_TAG

for all the repos that your repo depends on, add them as submodules of your repo

for each submodule <a>, the image name should be the same as the submodule dir name

the tag should be from envrionment variable <submodule>_<a>_TAG

all the tag has `-` replaced by `_`

##

send a pull request when you release a new version of your repo

# step-by-step to add a module
1. create <my-plugin> repo on pd  
2. clone pds-release repo
3. create pds-release/plugin/<my-plugin>.yml
  See "plugin configuration format for ${INIT_PLUGIN_PATH}" in https://github.com/RENCI/tx-router for documentation
4. make <my-plugin> a submodule of pds-release/sub-modules

# step-by-step to upgrade module
1. tag your own repo
2. send pull-request
