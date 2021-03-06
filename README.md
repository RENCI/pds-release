[![Build Status](https://travis-ci.com/RENCI/pds-release.svg?branch=master)](https://travis-ci.com/RENCI/pds-release)

pds: [![Build Status](https://travis-ci.com/RENCI/pds.svg?branch=master)](https://travis-ci.com/RENCI/pds)

pdspi-config: [![Build Status](https://travis-ci.com/RENCI/pdspi-config.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-config)

pdspi-fhir-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-fhir-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-fhir-example)

pdspi-mapper-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-mapper-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-mapper-example)

pdspi-mapper-parallex-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-mapper-parallex-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-mapper-parallex-example)

pdspi-guidance-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-guidance-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-guidance-example)

tx-logging: [![Build Status](https://travis-ci.com/RENCI/tx-logging.svg?branch=master)](https://travis-ci.com/RENCI/tx-logging)

tx-router: [![Build Status](https://travis-ci.com/RENCI/tx-router.svg?branch=master)](https://travis-ci.com/RENCI/tx-router)


# pds-release
Repo for facilitating coordinated release of multiple pds repos

Requires Python 3.8+

With conda, this works:
```
conda create -n pds python=3.8
conda activate pds
```


# step-by-step to add module
see developer guide

# step-by-step to upgrade module
see developer guide
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
Install fresh
```
git clone --recursive http://github.com/RENCI/pds-release
```

OR

Pull all submodules

```
git submodule update --init --recursive
```

Python 3.8 is required.
```
pip install -r requirements.txt
```
```
./up.sh
```
Be sure to configure `pds-release/test.system/env.pds` to suit your needs, particularly the `PDSPI_FHIR_EXAMPLE_FHIR_SERVER_URL_BASE` variable.

# tear down
```
./down.sh
```

# system testing
```
python system.py test
```

# enable fhir server

## from remote server

set `PDSPI_FHIR_EXAMPLE_FHIR_SERVER_URL_BASE` in `test.system/env.pds`

##  from local data 

### Ingest local data:

  ```
  cd module/pdspi-fhir-example
  PYTHONPATH=tx-utils/src:tx-pcornet-to-fhir/ python ingest.py --base_url http://localhost:8080/v1/plugin/pdspi-fhir-example --input_dir <pcornet_data_path> --input_data_format pcori --output_dir <fhir_data_path>
  ```
The PCORNet data in <pcornet_data_path> will be ingested into a docker-managed volume so it will persist between `./down.sh` and `./up.sh`. 

### Check ingestion

1. Manually inspect the FHIR format in <fhir_data_path>

2. Retrieve some records

Find a <patientid> in <fhir_data_path>/Patient/1000.json and run some queries:

```
curl http://localhost:8080/v1/plugin/pdspi-fhir-example/Patient/<patientid>
```

```
curl http://localhost:8080/v1/plugin/pdspi-fhir-example/MedicationRequest?patient=<patientid>
```

```
curl http://localhost:8080/v1/plugin/pdspi-fhir-example/Observation?patient=<patientid>
```


# set subnet

set `IPAM_CONFIG_SUBNET` in `module/tx-router/test/env.docker`

We recommend keeping a separate "Qualified installation" (QI) document locally to record the value(s) of the subnets used for your development, staging, and production servers. 

# set config

set `PDSPI_CONFIG_DEFAULT_CONFIG` in `test.system/env.pds`


# solving the dns error

try adding `network_mode="host"` in the call to `build` method call in `system.py`.
