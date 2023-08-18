import argparse
import os
import getpass
import platform
import subprocess
from pathlib import Path

DEFAULT_DOCKER_IMAGE = ""
DEFAULT_DOCKER_URL = ""

def touch_shell_setting_file():
   (Path.home() / ".mmcv_history").touch()

def is_local_image(image):
   return not run_subprocess(f"docker image inspect {image}", check=False).returncode

def fetch_image(docker_url, image):
   docker_image = f"{docker_url}/{image}"

   print(f"Trying to fetch '{docker_image}'. It might take a while........")   
   process = run_subprocess(f"docker pull {docker_image}", check=False, stdout=True)

   return docker_image

def run_subprocess(command, check):
   return subprocess.run(command, check=True)


def get_container_name(interactive):
   if interactive:
      whoami = getpass.getuser()
      return f"{whoami}-{datetime_str}"
   return "mmcv"

def get_mount(client_mounts):
   args = []
   if client_mounts:
      for(src,dst) in client_mounts:
         src = str(Path(src).resolve())
         assert os.path.exists(src), f"Host pash {src} does not exist!!!!!"
         args.extend(["-v", f"{src}:{dst}"])
   return args

def parse_client():
   parser = argparse.ArgumentParser(description=__doc__)
   parser.add_argument(
      "-u",
      "--docker-url",
      default=DEFAULT_DOCKER_URL,
      help=f"docker url."
   )
   parser.add_argument(
      "-i",
      "--image",
      default=DEFAULT_DOCKER_IMAGE,
      help=f"docker image name."
   )
   parser.add_argument("-x",action="store_true", help="allow local X11 commnu")
   parser.add_argument("-d",action="store_true", help="run in detached mode")
   
   parser.add_argument(
      "-v",
      action="append",
      metavar=("src","dest")
      help=f"Ex: -v /mnt/host_lol /mnt/dest_lol"
   )
   #parse.add_argument("-p",action="append", help="-p 8080'8080")
   return parser.parser_args()

def verify_non_root():
   if getpass.getuser() == "root":
      raise RuntimeError("Do not run this script as root")
   home_path = "/home" if platform.system() == "Linux" else "/Users"

   if Path(home_path) not in Path.home().parent:
      raise RuntimeError(
         f"Did not expect home dir to be {Path.home()}. Please run a user in '{home_path}'"
      )

def print_highlight(heading, value, color):
   color_map = {
      "red": ["\033[91m","\033[0m"],
      "green": ["\033[92m","\033[0m"],
   }
   cstart, cend = color_map[color]
   print(cstart+ heading.upper())
   print(value)
   print(cend)

def main():

   verify_non_root()
   
   args = parse_client()

   docker_image = fetch_image(args.docker_url, args.image)
   docker_args = ["docker","run"]

   docker_args += ["-d"] if args.d else ["-it"]
   docker_args.extend(["--name", get_container_name(not arg.d)])

   docker_args += get_default_docker_args()
   docker_args += get_mount(args.v)

   if args.x:
      run_subprocess(["xhost", "+"])
      docker_args += get_local_x11_args()

   if args.p:
      for port in args.p:
         docker_args += get_local_x11_args()
   
   docker_args += [docker_image]

   if platform.system() == "Linux":
      command = (
         f"chown -hR "
         f""
      )
      docker_args.extend(["/bin/bash", "-c"] + f'"{command}"'.split()) 
      subprocess.run("".join(docker_args), encoding="utf-8", shell=True,check=True)                    
   

if __name__ == "__main__":
   try:
      main()
   except RuntimeError as e:
      print_highlight("runtime error:", str(e))
   except subprocess.CalledProcessError as e:
      print_highlight("subprocess std error:", str(e.stderr))

