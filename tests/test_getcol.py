import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from malcolm3utils.scripts.getcol import getcol

TEST_INPUT = """A\tB\tC\tD
1\t2\t3\t4
"""


@pytest.fixture
def tmp_file(tmp_path: Path) -> Path:
    f_path = tmp_path.joinpath("test.csv")
    with open(os.path.join(f_path), "w") as fh:
        fh.write(TEST_INPUT)
    return f_path


def test_getcol(tmp_file: Path) -> None:
    runner = CliRunner()
    tmp_file_name = str(tmp_file)

    # noinspection PyTypeChecker
    result = runner.invoke(
        getcol,
        ["2", tmp_file_name],
    )
    assert result.exit_code == 0
    assert result.output == "B\n2\n"

    # noinspection PyTypeChecker
    result = runner.invoke(
        getcol,
        ["2,4", tmp_file_name],
    )
    assert result.exit_code == 0
    assert result.output == "B\tD\n2\t4\n"

    # noinspection PyTypeChecker
    result = runner.invoke(
        getcol,
        ["2-4", tmp_file_name],
    )
    assert result.exit_code == 0
    assert result.output == "B\tC\tD\n2\t3\t4\n"

    # noinspection PyTypeChecker
    result = runner.invoke(
        getcol,
        ["2,D", tmp_file_name],
    )
    assert result.exit_code == 0
    assert result.output == "B\tD\n2\t4\n"

    # noinspection PyTypeChecker
    result = runner.invoke(
        getcol,
        ["-o", "|", "2,BAD-HEADER,4"],
        input=TEST_INPUT,
    )
    assert result.exit_code == 0
    assert result.output == "B|D\n2|4\n"
