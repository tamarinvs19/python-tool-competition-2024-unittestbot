import pathlib
import site
import subprocess
import sys
import tempfile
import time


def _run_utbot(
        source_file: pathlib.Path,
        sys_paths: list[pathlib.Path],
        output_file: pathlib.Path,
        jar_path: pathlib.Path,
        usvm_dir: pathlib.Path,
        timeout: int,
        python_path: str,
        java_cmd: str,
):
    command = f"{java_cmd} -jar {jar_path} generate_python {source_file} -p {python_path} -o {output_file} -s {','.join(map(str, sys_paths))} -t {timeout} --java-cmd {java_cmd} --usvm-dir {usvm_dir} --runtime-exception-behaviour PASS --prohibited-exceptions - --check-usvm"
    print(command)

    p = subprocess.Popen(command.split(), close_fds=True)
    while p.poll() is None:
        time.sleep(1)


def main():
    with tempfile.TemporaryDirectory() as tempdir:
        output_dir = pathlib.Path(tempdir)
        output_file = output_dir / f"test_example1.py"
        site_dir = pathlib.Path(site.getsitepackages()[0])
        jar_file = site_dir / "utbot_dist" / "utbot-cli-python-2023.11-SNAPSHOT.jar"
        usvm_path = site_dir / "utbot_dist" / "usvm-python"
        python_path = sys.executable
        _run_utbot(
            pathlib.Path("./targets/example1.py"),
            [pathlib.Path("./targets/")],
            output_file,
            jar_file,
            usvm_path,
            20_000,
            python_path,
            "java"
        )
