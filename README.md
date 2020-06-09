[![Build Status](https://travis-ci.com/RENCI/pds-release.svg?branch=master)](https://travis-ci.com/RENCI/pds-release)

# pds-release
Repo for facilitating coordinated release of multiple pds repos

# step-by-step to add module
1. fork
1. tag your own repo
1. add you own repo as submmodule to under `module`
1. update system integration testing as needed
1. run tests 
```hooks/test```
1. commit
1. push to your fork
1. send pull request

# step-by-step to upgrade module
1. fork
1. tag new version your own repo
1. pull you new version to under `module`
1. update system integration testing as needed
1. run tests 
```hooks/test```
1. commit
1. push to your fork
1. send pull request

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


# stand up
Python 3.8 is required.
```
pip install -r requirements.txt
```

```
./up.sh
```

# tear down
```
./down.sh
```
