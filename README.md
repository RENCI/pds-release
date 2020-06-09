[![Build Status](https://travis-ci.com/RENCI/pds-release.svg?branch=master)](https://travis-ci.com/RENCI/pds-release)

# pds-release
Repo for facilitating coordinated release of multiple pds repos


# how to add your repo in a release

## add submodule
Add your repo as a submodule under the `module` dir

If your repo have a `Dockerfile`, then a docker image will be built using that `Dockerfile`

### Automatic tag discovery

If your repo have a tag `<tag>`, then the docker image will be tagged with `<tag>`, otherwise, the hash is going to be used as the tag.

## add yml

Add a yml file under the `plugin` dir

how to write the yml file

see example under `plugin/pds.yml`

the image name should be the same as the submodule dir name

the tag should be from envrionment variable `<submodule>_TAG`

for all the images that your repo depends on, you can either specify an image with in a remote repo or you can add them as submodules of your repo to utilized the automatic tag discovery mechanism

for each submodule `<a>`, the image name should be the same as the submodule dir name and the tag should be from envrionment variable `<submodule>_<a>_TAG`

all the tag has `-` replaced by `_`

For example, 

```
services:
  a:
    image: a-b:${a_b_TAG}
  b:
    image: c-d:${a_b_c_d_TAG}
    
```

## send a pull request

send a pull request when you release a new version of your repo

## stand up
Python3 is required.
```
pip install -r requirements.txt
```

```
./up.sh
```

## tear down
```
./down.sh
```

# step-by-step to add a module
1. create <my-plugin> repo on pd  
2. clone pds-release repo
3. create pds-release/plugin/<my-plugin>.yml
  See "plugin configuration format for ${INIT_PLUGIN_PATH}" in https://github.com/RENCI/tx-router for documentation
4. make <my-plugin> a submodule of pds-release/sub-modules

# step-by-step to upgrade module
1. tag your own repo
2. send pull-request
