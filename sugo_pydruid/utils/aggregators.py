#
# Copyright 2013 Metamarkets Group Inc.
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
from six import iteritems

from .filters import Filter


def longsum(raw_metric):
    return {"type": "lucene_longSum", "fieldName": raw_metric}


def doublesum(raw_metric):
    return {"type": "lucene_doubleSum", "fieldName": raw_metric}


def longmin(raw_metric):
    return {"type": "lucene_longMin", "fieldName": raw_metric}


def longmax(raw_metric):
    return {"type": "lucene_longMax", "fieldName": raw_metric}


def doublemin(raw_metric):
    return {"type": "lucene_doubleMin", "fieldName": raw_metric}


def doublemax(raw_metric):
    return {"type": "lucene_doubleMax", "fieldName": raw_metric}


def count():
    return {"type": "lucene_count"}


def hyperunique(raw_metric):
    return {"type": "lucene_hyperUnique", "fieldName": raw_metric}


def cardinality(raw_column, by_row=False):
    if type(raw_column) is not list:
        raw_column = [raw_column]
    return {"type": "lucene_cardinality", "fieldNames": raw_column, "byRow": by_row}


def filtered(filter, agg):
    return {"type": "lucene_filtered",
            "filter": Filter.build_filter(filter),
            "aggregator": agg}

def javascript(columns_list, fn_aggregate, fn_combine, fn_reset):
    return {"type": "lucene_javascript",
            "fieldNames": columns_list,
            "fnAggregate":fn_aggregate,
            "fnCombine":fn_combine,
            "fnReset":fn_reset}

def build_aggregators(agg_input):
    return [_build_aggregator(name, kwargs)
            for (name, kwargs) in iteritems(agg_input)]


def _build_aggregator(name, kwargs):
    if kwargs["type"] == "lucene_filtered":
        kwargs["aggregator"] = _build_aggregator(name, kwargs["aggregator"])
    else:
        kwargs.update({"name": name})

    return kwargs