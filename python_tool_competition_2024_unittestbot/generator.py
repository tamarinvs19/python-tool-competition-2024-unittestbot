"""A test generator using UnitTestBot."""
import os
import pathlib
import site
import subprocess
import sys
import tempfile
import threading
import time

import rich
from python_tool_competition_2024.config import get_config, GeneratorName
from python_tool_competition_2024.generation_results import (
    TestGenerationFailure,
    TestGenerationResult,
    TestGenerationSuccess,
    FailureReason,
)
from python_tool_competition_2024.generators import FileInfo, TestGenerator


class UnittestbotTestGenerator(TestGenerator):
    """A test generator using UnitTestBot."""

    java_path = "java"

    def build_test(self, target_file_info: FileInfo) -> TestGenerationResult:
        """
        Generate a test for the specific target file.

        Args:
            target_file: The `FileInfo` of the file to generate a test for.

        Returns:
            Either a `TestGenerationSuccess` if it was successful, or a
            `TestGenerationFailure` otherwise.
        """
        if not sys.platform.startswith("linux"):
            sys.stderr.write("ERROR: This script works only on Linux\n")
            exit(1)

        site_dir = pathlib.Path(site.getsitepackages()[0])
        jar_file = site_dir / "utbot_dist" / "utbot-cli-python-2023.11-SNAPSHOT.jar"
        usvm_path = site_dir / "utbot_dist" / "usvm-python"

        sys_paths = [target_file_info.config.targets_dir]
        python_path = sys.executable

        with tempfile.TemporaryDirectory() as tempdir:
            output_dir = pathlib.Path(tempdir)
            module_name = target_file_info.module_name.replace(".", "_")
            output_file = output_dir / f"test_{module_name}.py"
            timeout = 90_000
            _run_utbot(
                target_file_info.absolute_path,
                sys_paths,
                output_file,
                jar_file,
                usvm_path,
                timeout,
                python_path,
                self.java_path,
            )

            utbot_tests = _read_generated_tests(str(output_file))
            if utbot_tests == "":
                return TestGenerationFailure(tuple(), FailureReason.NOTHING_GENERATED)

            return TestGenerationSuccess(utbot_tests)


times = []


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
    command = f"{java_cmd} -jar {jar_path} generate_python {source_file} -p {python_path} -o {output_file} -s {','.join(map(str, sys_paths))} -t {timeout} --java-cmd {java_cmd} --usvm-dir {usvm_dir} --runtime-exception-behaviour PASS --prohibited-exceptions -"
    print(command)
    start = time.time()

    p = subprocess.Popen(command.split(), close_fds=True)
    while p.poll() is None:
        time.sleep(1)
    
    cur_time = time.time() - start
    times.append(cur_time)
    print("Process finished in", cur_time)
    print("Mean time:", sum(times) / len(times))
    print("Max time:", max(times))


def _read_generated_tests(output_file: str) -> str:
    try:
        with open(output_file, "r") as f:
            return f.read()
    except:
        return ""


if __name__ == "__main__":
    test_code = UnittestbotTestGenerator().build_test(
            FileInfo(
                pathlib.Path(
                    "../targets/example1.py"
                ).absolute(),
                "example1",
                get_config(
                    GeneratorName("Unittestbot"),
                    pathlib.Path("../targets").absolute(),
                    pathlib.Path("").absolute(),
                    rich.console.Console(),
                    show_commands=True,
                    show_failures=True,
                ),
            )
        )
    if isinstance(test_code, TestGenerationSuccess):
        print(test_code.body)

