import os
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import pytest
from click.testing import CliRunner

from medutils.scripts.touch_latest import touch_latest

now = int(datetime.now().timestamp())


class FileEntry(TypedDict):
    name: str
    mtime: int


tmp_tree_files: list[FileEntry] = [
    {
        'name': 'file.1990.01.01',
        'mtime': int(datetime(1990, 1, 1).timestamp())
    },
    {
        'name': 'file.2000.03.03',
        'mtime': int(datetime(2000, 3, 3).timestamp())
    },
    {
        'name': 'file.2010.05.05',
        'mtime': int(datetime(2010, 5, 5).timestamp())
    },
    {
        'name': 'ignore.~1~',
        'mtime': now
    },
    {
        'name': 'ignore.JUNK',
        'mtime': now
    },
    {
        'name': 'ignore.GARBAGE',
        'mtime': now
    },

]


@pytest.fixture
def tmp_tree(tmp_path: Path) -> Path:
    d = tmp_path / 'sub'
    d.mkdir()
    for entry in tmp_tree_files:
        f_path = d / entry['name']
        f_path.touch()
        os.utime(f_path, (now, int(entry['mtime'])))
    ignore_file = tmp_path / 'ignore'
    dd = d / 'subsub'
    dd.mkdir()
    ff_path = dd / 'ignore.TRASH'
    ff_path.touch()
    with open(ignore_file, 'w') as fh:
        fh.write('*.GARBAGE\nsubsub/*.TRASH\n')
    return tmp_path


def test_touch_latest(tmp_tree: Path) -> None:
    runner = CliRunner()
    search_dir = tmp_tree / 'sub'
    touch_file = tmp_tree / 'latest'
    ignore_file = tmp_tree / 'ignore'
    # noinspection PyTypeChecker
    result = runner.invoke(touch_latest, ['-i', '*.JUNK', '-f', str(ignore_file), str(touch_file), str(search_dir)])
    assert result.exit_code == 0
    assert result.output == ''
    touch_file_stat = touch_file.stat()
    assert touch_file_stat.st_mtime == tmp_tree_files[2]['mtime']
    # import time
    # time.sleep(600)
