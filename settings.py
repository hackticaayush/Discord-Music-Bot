import os
from dotenv import load_dotenv
import subprocess
import sys
import platform

work_dir = os.getcwd()
os_name = platform.system()
opus_zip_name = "opus-1.5.2"
opus_zip_full_name = "opus-1.5.2.tar.gz"

if os_name == "Darwin":
    libopus_build_file_name = "libopus.dylib"
    commands = [
    f'''cd opus
    tar -xzf {opus_zip_full_name}
    cd {opus_zip_name}
    brew install meson ninja
    mkdir build
    cd build
    meson ..
    ninja
    sudo ninja install
    cp src/{libopus_build_file_name} {work_dir}/libs/
    cd {work_dir}
    sudo rm -r opus/{opus_zip_name}/'''
    ]
elif os_name == "Linux":
    libopus_build_file_name = "libopus.so"
    commands = [
    f'''cd opus
    tar -xzf {opus_zip_full_name}
    cd {opus_zip_name}
    sudo apt install meson ninja
    mkdir build
    cd build
    meson setup ..
    ninja
    sudo ninja install
    cp src/{libopus_build_file_name} {work_dir}/libs/
    cd {work_dir}
    sudo rm -r opus/{opus_zip_name}'''
    ]

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()

if not os.path.exists(f"{work_dir}/libs/{libopus_build_file_name}"):
    for cmd in commands:
        run_command(cmd)


def install_requirements()->bool:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)
install_requirements()

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")