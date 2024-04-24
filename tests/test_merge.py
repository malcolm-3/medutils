import logging
from datetime import datetime
from pathlib import Path
from typing import List, TypedDict

import pytest
from click.testing import CliRunner

from medutils.scripts.merge import merge

logger = logging.getLogger(__name__)

now = int(datetime.now().timestamp())


class FileEntry(TypedDict):
    name: str
    mtime: int


EXPECTED_HELP = """Usage: merge [OPTIONS] [FILES_TO_READ]...

  Merge the specified delimited files with column headings, joining entries with
  the same key field value.

  The files do not need to be sorted on the key field as with join(1). This does
  require that all of the data be read into memory. If that is a problem, using
  the system join(1) command is recommended.

  Rows will be printed in the order that the unique key values are encountered
  when reading through the input files.

  To read from stdin, use '-' as the filename.

  The output key column will be the first column of the output file and the
  header will be the header from the first file.

  If -k is used to specify alternative keys columns for subsequent files, but
  those files have a column with the same name as the output key column, that
  will be ignored.

Options:
  -v, --verbosity LVL          Either CRITICAL, ERROR, WARNING, INFO or DEBUG.
  -d, --delimiter TEXT         column delimiter (default=TAB)
  -o, --output-delimiter TEXT  output column delimiter (default=input delimiter)
  --all-delimiter TEXT         when keep=="all" this will be the delimiter
                               between entries where there are multiple
                               (default=";")
  -k, --key-column TEXT        comma separated list of key column identifiers.
                               each new file will use the next identifier. the
                               last identifier will be used for all remaining
                               files, so just use "-k identifier" if the
                               identifier is the same for all files. The
                               identifier can either be the header string or the
                               one-based column index. (default=1 (i.e. the
                               first column of each file))
  --keep [first|last|all]      specifies how to handle multiple values for the
                               same field with the same key
  -I, --ignore TEXT            comma separated list of column identifiers to
                               ignore
  --help                       Show this message and exit.
"""

FILE1 = """Key\tF1\tF2
a\t1af1\t1af2
b\t1bf1\t1bf2
c\t1cf1\t
d\t\t1df2
"""

FILE2 = """AltKey\tKey\tF3\tF2
d\ta\t2af3\t2af2
c\tb\t2bf3\t2bf2
b\tc\t2cf3\t
a\td\t\t2df2
e\te\t2ef3\t2ef2
"""

FILE3 = """X\tY\tZ
a\t3ay\t3az
b\t3by\t3bz"""

FILE4 = """AltKey\tKey\tF3\tF2
d\ta\t2af3\t2af2
c\tb\t2bf3\t2bf2
\t\tx\tx
b\tc\t2cf3\t
a\td\t\t2df2
e\te\t2ef3\t2ef2
"""

EXPECTED_FIRST = """Key\tF1\tF2\tAltKey\tF3
a\t1af1\t1af2\td\t2af3
b\t1bf1\t1bf2\tc\t2bf3
c\t1cf1\t\tb\t2cf3
d\t\t1df2\ta\t
e\t\t2ef2\te\t2ef3
"""

EXPECTED_ALL = """Key\tF1\tF2\tAltKey\tF3
a\t1af1\t1af2;2af2\td\t2af3
b\t1bf1\t1bf2;2bf2\tc\t2bf3
c\t1cf1\t\tb\t2cf3
d\t\t1df2;2df2\ta\t
e\t\t2ef2\te\t2ef3
"""

EXPECTED_LAST = """Key\tF1\tF2\tAltKey\tF3
a\t1af1\t2af2\td\t2af3
b\t1bf1\t2bf2\tc\t2bf3
c\t1cf1\t\tb\t2cf3
d\t\t2df2\ta\t
e\t\t2ef2\te\t2ef3
"""

EXPECTED_ALL_COMMA = EXPECTED_ALL.replace("\t", ",")

EXPECTED_ALL_ALTKEY = """Key\tF1\tF2\tF3
a\t1af1\t1af2;2df2\t
b\t1bf1\t1bf2\t2cf3
c\t1cf1\t2bf2\t2bf3
d\t\t1df2;2af2\t2af3
e\t\t2ef2\t2ef3
"""

EXPECTED_ALL_IGNORE = """Key\tF2\tF3
a\t1af2;2af2\t2af3
b\t1bf2;2bf2\t2bf3
c\t\t2cf3
d\t1df2;2df2\t
e\t2ef2\t2ef3
"""

tmp_tree_files: list[FileEntry] = [
    {"name": "file.1990.01.01", "mtime": int(datetime(1990, 1, 1).timestamp())},
    {"name": "file.2000.03.03", "mtime": int(datetime(2000, 3, 3).timestamp())},
    {"name": "file.2010.05.05", "mtime": int(datetime(2010, 5, 5).timestamp())},
    {"name": "ignore.~1~", "mtime": now},
    {"name": "ignore.JUNK", "mtime": now},
    {"name": "ignore.GARBAGE", "mtime": now},
]


@pytest.fixture
def tmp_files(tmp_path: Path) -> List[Path]:
    f1 = tmp_path.joinpath("file1")
    with open(f1, "w") as fh:
        fh.write(FILE1)
    f2 = tmp_path.joinpath("file2")
    with open(f2, "w") as fh:
        fh.write(FILE2)
    f3 = tmp_path.joinpath("file3")
    with open(f3, "w") as fh:
        fh.write(FILE3)
    f4 = tmp_path.joinpath("file4")
    with open(f4, "w") as fh:
        fh.write(FILE4)
    return [f1, f2, f3, f4]


def test_merge(tmp_files: List[Path]) -> None:
    runner = CliRunner()
    file1 = str(tmp_files[0])
    file2 = str(tmp_files[1])
    file3 = str(tmp_files[2])
    file4 = str(tmp_files[3])

    logger.debug("check help output")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["--help"],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_HELP

    logger.debug("check without key")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        [file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL_ALTKEY

    logger.debug("check with key")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL

    logger.debug("check without per file key")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key,AltKey", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL_ALTKEY

    logger.debug("check with key, keep==first")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key", "--keep", "first", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_FIRST

    logger.debug("check with key, keep==last")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key", "--keep", "last", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_LAST

    logger.debug("check with key, reading stdin")
    # noinspection PyTypeChecker
    result = runner.invoke(merge, ["-k", "Key", file1, "-"], input=FILE2)
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL

    logger.debug("check with key, change output delimiter")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key", "-o", ",", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL_COMMA

    logger.debug("check with key, bad file")
    # noinspection PyTypeChecker
    result = runner.invoke(merge, ["-k", "Key", file1, file3, file2], input=FILE2)
    assert result.exit_code == 0
    output_lines = result.output.split("\n")
    stderr_line = output_lines.pop(0)
    stdout = "\n".join(output_lines)
    assert stdout == EXPECTED_ALL
    assert stderr_line.startswith('warning: Key "Key" not found')

    logger.debug("check with key, bad row")
    # noinspection PyTypeChecker
    result = runner.invoke(merge, ["-k", "Key", file1, file4], input=FILE2)
    assert result.exit_code == 0
    output_lines = result.output.split("\n")
    stderr_line = output_lines.pop(0)
    stdout = "\n".join(output_lines)
    assert stdout == EXPECTED_ALL
    assert stderr_line.startswith("warning: No key value found for line 4")

    logger.debug("check with key, empty file")
    result = runner.invoke(merge, ["-k", "Key", file1, "-", file2], input="")
    assert result.exit_code == 0
    output_lines = result.output.split("\n")
    stderr_line = output_lines.pop(0)
    stdout = "\n".join(output_lines)
    assert stdout == EXPECTED_ALL
    assert stderr_line.startswith("warning: No fieldnames found in file")

    logger.debug("check with key, ignore")
    # noinspection PyTypeChecker
    result = runner.invoke(
        merge,
        ["-k", "Key", "-I", "F1,AltKey", file1, file2],
    )
    assert result.exit_code == 0
    assert result.output == EXPECTED_ALL_IGNORE
