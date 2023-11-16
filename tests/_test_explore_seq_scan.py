from explore import QEP
from utils import assert_test


def test_seq_scan_filter_like():
    op = {
        "Node Type": "Seq Scan",
        "Parent Relationship": "Outer",
        "Parallel Aware": True,
        "Async Capable": False,
        "Relation Name": "part",
        "Schema": "public",
        "Alias": "part",
        "Startup Cost": 0.00,
        "Total Cost": 5138.67,
        "Plan Rows": 5892,
        "Plan Width": 4,
        "Actual Startup Time": 0.579,
        "Actual Total Time": 23.182,
        "Actual Rows": 3555,
        "Actual Loops": 3,
        "Output": ["part.p_partkey", "part.p_name", "part.p_mfgr", "part.p_brand", "part.p_type", "part.p_size", "part.p_container", "part.p_retailprice", "part.p_comment"],
        "Filter": "((part.p_name)::text ~~ '%green%'::text)",
        "Rows Removed by Filter": 63112,
        "Workers": [
            {
                "Worker Number": 0,
                "Actual Startup Time": 0.744,
                "Actual Total Time": 15.468,
                "Actual Rows": 2155,
                "Actual Loops": 1
            },
            {
                "Worker Number": 1,
                "Actual Startup Time": 0.957,
                "Actual Total Time": 13.027,
                "Actual Rows": 1720,
                "Actual Loops": 1
            }
        ]
    }
    QEP(op).resolve()
    assert_test(op)