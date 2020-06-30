# Lint as: python3

# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Creates a pandas DataFrame accessor for TFRUtil.

accessor.py contains TFRUtilAccessor which provides a pandas DataFrame
accessor.  This accessor allows us to inject the to_tfr() function into
pandas DataFrames.
"""
from typing import Any, Dict, Optional, Union
import pandas as pd

from tfrutil import client


@pd.api.extensions.register_dataframe_accessor("tensorflow")
class TFRUtilAccessor:
  """DataFrame Accessor class for TFRUtil."""

  def __init__(self, pandas_obj):
    self._df = pandas_obj

  # pylint: disable=too-many-arguments
  def to_tfr(
      self,
      output_dir: str,
      runner: str = "DirectRunner",
      project: Optional[str] = None,
      region: Optional[str] = None,
      tfrutil_path: Optional[str] = None,
      dataflow_options: Union[Dict[str, Any], None] = None,
      job_label: str = "to-tfr",
      compression: Optional[str] = "gzip",
      num_shards: int = 0):
    """TFRUtil Pandas Accessor.

    TFRUtil provides an easy interface to create image-based tensorflow records
    from a dataframe containing GCS locations of the images and labels.

    Usage:
      import tfrutil

      df.tfrutil.to_tfr(
          output_dir="gcs://foo/bar/train",
          runner="DirectRunner",
          compression="gzip",
          num_shards=10)

    Args:
      output_dir: Local directory or GCS Location to save TFRecords to.
      runner: Beam runner. Can be DirectRunner or  DataFlowRunner.
      project: GCP project name (Required if DataFlowRunner).
      region: GCP region name (Required if DataFlowRunner).
      tfrutil_path: Path to tfrutil source (Required if DataFlowRunner).
      dataflow_options: Optional dictionary containing DataFlow options.
      job_label: User supplied description for the beam job name.
      compression: Can be "gzip" or None for no compression.
      num_shards: Number of shards to divide the TFRecords into. Default is
          0 = no sharding.

    """
    client.create_tfrecords(
        self._df,
        output_dir=output_dir,
        runner=runner,
        project=project,
        region=region,
        tfrutil_path=tfrutil_path,
        dataflow_options=dataflow_options,
        job_label=job_label,
        compression=compression,
        num_shards=num_shards)
    #TODO (mikebernico) Add notebook output for user.
