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

import pathlib

from pydax import get_config, init
from pydax.dataset import Dataset


def test_default_data_dir(loaded_schemata):
    "Test to make sure Dataset will use default global data dir if nothing passed to pydax.init or Dataset constructor."

    pydax_data_home = pathlib.Path.home() / '.pydax' / 'data'
    assert get_config().DATADIR == pydax_data_home
    schema = loaded_schemata.schemata['dataset_schema'].export_schema('datasets', 'wikitext103', '1.0.1')
    wikitext = Dataset(schema, mode=Dataset.InitializationMode.LAZY)
    assert wikitext._data_dir == pydax_data_home


def test_custom_data_dir(tmp_path, loaded_schemata):
    "Test to make sure Dataset constructor uses new global data dir if one was supplied earlier to pydax.init."

    init(DATADIR=tmp_path)
    assert get_config().DATADIR == tmp_path
    schema = loaded_schemata.schemata['dataset_schema'].export_schema('datasets', 'wikitext103', '1.0.1')
    wikitext = Dataset(schema, mode=Dataset.InitializationMode.LAZY)
    assert wikitext._data_dir == tmp_path
