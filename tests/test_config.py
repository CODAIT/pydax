#
# Copyright 2020 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import pathlib
import re

import pytest
from pydantic import ValidationError

from pydax import get_config, init
from pydax.dataset import Dataset


def test_default_data_dir(wikitext103_schema):
    "Test default data dir."

    pydax_data_home = pathlib.Path.home() / '.pydax' / 'data'
    assert get_config().DATADIR == pydax_data_home
    assert isinstance(get_config().DATADIR, pathlib.Path)


def test_custom_data_dir(tmp_path, wikitext103_schema):
    "Test to make sure Dataset constructor uses new global data dir if one was supplied earlier to pydax.init."

    init(DATADIR=tmp_path)
    assert get_config().DATADIR == tmp_path
    assert isinstance(get_config().DATADIR, pathlib.Path)
    wikitext = Dataset(wikitext103_schema, data_dir=tmp_path, mode=Dataset.InitializationMode.LAZY)
    assert wikitext._data_dir == tmp_path
    assert isinstance(wikitext._data_dir, pathlib.Path)


def test_custom_relative_data_dir(tmp_path):
    "Test using a custom relative data directory."

    init(DATADIR=os.path.relpath(tmp_path))
    assert get_config().DATADIR == tmp_path
    assert get_config().DATADIR.is_absolute()


def test_custom_symlink_data_dir(tmp_symlink_dir):
    "Test using a custom symlink data directory. The symlink should not be resolved."

    init(DATADIR=tmp_symlink_dir)
    assert get_config().DATADIR == tmp_symlink_dir


def test_non_path_data_dir():
    "Test exception when a nonpath is passed as DATADIR."

    with pytest.raises(ValidationError) as e:
        init(DATADIR=10)

    assert re.search(r"1 validation error for Config\s+DATADIR\s+value is not a valid path \(type=type_error.path\)",
                     str(e.value))
