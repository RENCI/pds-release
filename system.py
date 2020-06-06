import os
import os.path
import sys
import shutil
import subprocess
import logging
from envbash import load_envbash
import docker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

cmd, *_ = sys.argv[1:]

cwd = os.getcwd()

docker_client = docker.from_env()

env = {}

def git_tag(submodule_dir):
    a = subprocess.run(["git", "tag"], capture_output=True, cwd=submodule_dir)
    a.check_returncode()
    tag = a.stdout.decode("utf-8").split("\n")[0].strip()
    if tag == "":
        logger.warning(f"submodule at {submodule_dir} does not have a tag, use hash")
        a = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, cwd=submodule_dir)
        a.check_returncode()
        tag = a.stdout.decode("utf-8").strip()
    else:
        logger.info(f"submodule at {submodule_dir} tag {tag}")
    return tag

def get_submodule_version(submodules, submodule_dir):
    logger.info(f"looking at {submodules} in dir {submodule_dir}")
    tag = git_tag(submodule_dir)
    if os.path.isfile(os.path.join(submodule_dir, "Dockerfile")):
        env[f"{'_'.join(list(map(lambda s:s.replace('-', '_'), submodules)))}_TAG"] = tag
        build_docker_image(submodules[-1], tag, submodule_dir)

    b = subprocess.run(["git", "submodule", "status"], capture_output=True, cwd=submodule_dir)
    b.check_returncode()
    for submodulerow0 in b.stdout.decode("utf-8").split("\n"):
        # logger.info(f"submodulerow0 {submodulerow0}")
        submodulerow = submodulerow0.strip()
        if submodulerow != "":
            submodule = submodulerow.split(" ")[1]
            subsubmodule_dir = os.path.join(submodule_dir, submodule)
            get_submodule_version(submodules + [os.path.basename(submodule)], subsubmodule_dir)
    logger.info(f"done {submodule_dir}")


def build_docker_image(submodule, tag, submodule_dir):
    image = f"{submodule}:{tag}"
    logger.info(f"building image {image} at {submodule_dir}")
    docker_client.images.build(path=submodule_dir, tag=image)
    logger.info(f"done building {image}")
        

if os.path.isdir("module"):
    for submodule in os.listdir("module"):
        submodule_dir = os.path.join(cwd, "module", submodule)
        get_submodule_version([submodule], submodule_dir)

build = os.environ.get("build", "build")
os.makedirs(build, exist_ok=True)

shutil.copytree("module/tx-router", f"{build}/tx-router", dirs_exist_ok=True)
shutil.copytree("plugin", f"{build}/tx-router/plugin", dirs_exist_ok=True)
shutil.copy("test.system/env.pds", f"{build}/tx-router/env.txrouter")
logger.info(f"setting env to {env}")
os.environ.update(env)
with open(f"{build}/tx-router/env.txrouter", "a") as f:
    f.write("\n")
    for k, v in env.items():
        f.write(f"{k}={v}\n")
shutil.copy("test.system/docker-compose.system.yml", f"{build}/tx-router/test")
shutil.copy("test.system/Dockerfile.system", f"{build}/tx-router/test")
shutil.copy("test.system/test_func.system.py", f"{build}/tx-router/test")

os.chdir(build)

load_envbash("tx-router/test/env.docker")
os.environ["INIT_PLUGIN_PATH"] = "./plugin"
os.environ["MONGO_INITDB_ROOT_PASSWORD"] = "example"
os.environ["MONGO_NON_ROOT_PASSWORD"] = "collection"
os.environ["JWT_SECRET"] = "secret"

os.chdir("tx-router")

if cmd == "deploy":
    a = subprocess.run(["docker-compose", "-f", "docker-compose.yml", "-f", "nginx/unsecure/docker-compose.yml", "up", "--build", "-V", "-t", "3000", "-d"])
    a.check_returncode()
elif cmd == "down":
    a = subprocess.run(["docker-compose", "-f", "docker-compose.yml", "-f", "nginx/unsecure/docker-compose.yml", "down", "-t", "3000"])
    a.check_returncode()
elif cmd == "keep_containers":
    a = subprocess.run(["docker-compose", "-f", "docker-compose.yml", "-f", "nginx/unsecure/docker-compose.yml", "-f", "test/docker-compose.system.yml", "up", "--build", "-V", "-t", "3000"])
    a.check_returncode()
elif cmd == "test":
    a = subprocess.run(["docker-compose", "-f", "docker-compose.yml", "-f", "nginx/unsecure/docker-compose.yml", "-f", "test/docker-compose.system.yml", "up", "--build", "-V", "-t", "3000", "--exit-code-from", "pdsaggregator-test"])
    a.check_returncode()



