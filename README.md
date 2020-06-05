# pds-release
Repo for facilitating coordinated release of multiple pds repos


# how to add your repo in a release

Add your repo as a submodule

Your repo should have a Dockerfile

Your repo should also have a tag vx.y.z

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
