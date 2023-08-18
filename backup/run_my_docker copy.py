import argparse
import os
import getpass
import platform
import subprocess
from pathlib import Path
import datetime
from typing import List, Optional, Sequence, Tuple, Union

DEFAULT_DOCKER_IMAGE = "pyimage:20230531"

def touch_shell_setting_file():
   (Path.home() / ".mmcv_history").touch()

def run_subprocess(
   command: Union[str, Sequence[str]], 
   check: bool = True,
   stdout: bool = False,
   **kwargs,
) -> subprocess.CompletedProcess:
   if not stdout:
      kwargs["stdout"] = subprocess.PIPE
   return subprocess.run(
      command, 
      check=check,
      shell=True,
      encoding="utf-8",
      stderr=subprocess.PIPE,
      **kwargs,
   )

def is_local_image(image):
   return not run_subprocess(f"docker image inspect {image}", check=False).returncode


def get_container_name():
   """
   Get the docker container name.
   """
   whoami = getpass.getuser()
   datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
   return f"{whoami}-{datetime_str}"
   #return f"{datetime_str}"

   #if interactive:
   #   whoami = getpass.getuser()
   #   datetime_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
   #   return f"{whoami}-{datetime_str}"
   #return "mmcv"

def get_mount(client_mounts: Optional[List[Tuple[str,str]]]) -> List[str]:
   """
   Generate arguments to pass custom data mount from host src to a container path dest.
   """
   args = []

   if client_mounts:
      for(src,dst) in client_mounts:
         src = str(Path(src).resolve())
         assert os.path.exists(src), f"Host pash {src} does not exist!!!!!"
         args.extend(["-v", f"{src}:{dst}"])
   return args

def get_default_docker_args() -> List[str]:
   """
   Get the default docker arguments.
   """
   args = []

   args.extend(["-v", f"{Path(__file__).parent.absolute()}:/home/devel"])
   
   return args

def print_highlight(heading: str, value: str, color: str = "red") -> None:
   color_map = {
      "red": ["\033[91m","\033[0m"],
      "green": ["\033[92m","\033[0m"],
   }
   cstart, cend = color_map[color]
   print(cstart+ heading.upper())
   print(value)
   print(cend)

def parse_client() -> argparse.Namespace:
   """
   Parse Commandlist argument.
   """
   parser = argparse.ArgumentParser(description=__doc__)

   parser.add_argument(
      "-i",
      "--image",
      default=DEFAULT_DOCKER_IMAGE,
      help=f"docker image name."
   )

   parser.add_argument("-d",action="store_true", help="run in detached mode")
   
   parser.add_argument(
      "-v",
      action="append",
      #metavar=("src","dest"),
      help="",
   )
   parser.add_argument("-p",action="append", help="-p 8080'8080")

   return parser.parse_args()

def main():
   args = parse_client()

   docker_args = ["docker", "run"]
   docker_args += get_default_docker_args()
   docker_args += get_mount(args.v)
   
   docker_args += ["-it"]
   docker_args.extend(["--name=",DEFAULT_DOCKER_IMAGE])

   docker_args.extend(["/bin/bash"])
   #print(docker_args)

   container_name = get_container_name()
   print(container_name)

   print_highlight("running dokcer with:", " ".join(docker_args), color="green")
   #subprocess.run(" ".join(docker_args), encoding="utf-8", shell=True, check=True)

   local_image = is_local_image(DEFAULT_DOCKER_IMAGE)
   print(local_image)

if __name__ == "__main__":
   try:
      main()
   except RuntimeError as e:
      print_highlight("runtime error:", str(e))
   except subprocess.CalledProcessError as e:
      print_highlight("subprocess std error:", str(e.stderr))

