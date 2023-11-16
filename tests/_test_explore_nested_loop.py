from explore import QEP
from utils import assert_test


def test_seq_scan_index_only_scan():
    op = {
        "Node Type": "Nested Loop",
        "Parent Relationship": "Outer",
        "Parallel Aware": False,
        "Async Capable": False,
        "Join Type": "Inner",
        "Startup Cost": 0.42,
        "Total Cost": 11970.83,
        "Plan Rows": 23568,
        "Plan Width": 12,
        "Actual Startup Time": 1.124,
        "Actual Total Time": 37.431,
        "Actual Rows": 14219,
        "Actual Loops": 3,
        "Output": ["part.p_partkey", "partsupp.ps_suppkey", "partsupp.ps_partkey"],
        "Inner Unique": False,
        "Workers": [
            {
                "Worker Number": 0,
                "Actual Startup Time": 1.424,
                "Actual Total Time": 26.677,
                "Actual Rows": 8620,
                "Actual Loops": 1
            },
            {
                "Worker Number": 1,
                "Actual Startup Time": 1.895,
                "Actual Total Time": 22.127,
                "Actual Rows": 6880,
                "Actual Loops": 1
            }
        ],
        "Plans": [
            {
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
            },
            {
                "Node Type": "Index Only Scan",
                "Parent Relationship": "Inner",
                "Parallel Aware": False,
                "Async Capable": False,
                "Scan Direction": "Forward",
                "Index Name": "partsupp_pkey",
                "Relation Name": "partsupp",
                "Schema": "public",
                "Alias": "partsupp",
                "Startup Cost": 0.42,
                "Total Cost": 1.12,
                "Plan Rows": 4,
                "Plan Width": 8,
                "Actual Startup Time": 0.003,
                "Actual Total Time": 0.003,
                "Actual Rows": 4,
                "Actual Loops": 10664,
                "Output": ["partsupp.ps_partkey", "partsupp.ps_suppkey"],
                "Index Cond": "(partsupp.ps_partkey = part.p_partkey)",
                "Rows Removed by Index Recheck": 0,
                "Heap Fetches": 0,
                "Workers": [
                    {
                        "Worker Number": 0,
                        "Actual Startup Time": 0.004,
                        "Actual Total Time": 0.005,
                        "Actual Rows": 4,
                        "Actual Loops": 2155
                    },
                    {
                        "Worker Number": 1,
                        "Actual Startup Time": 0.004,
                        "Actual Total Time": 0.005,
                        "Actual Rows": 4,
                        "Actual Loops": 1720
                    }
                ]
            }
        ]
    }
    QEP(op, save=True).resolve()
    assert_test(op)


def _test_join_filter_seq_scan_seq_scan():
    op = {
        "Node Type": "Nested Loop",
        "Parallel Aware": False,
        "Async Capable": False,
        "Join Type": "Inner",
        "Startup Cost": 0.00,
        "Total Cost": 25834.13,
        "Plan Rows": 1690000,
        "Plan Width": 578,
        "Actual Startup Time": 0.019,
        "Actual Total Time": 62.520,
        "Actual Rows": 240000,
        "Actual Loops": 1,
        "Output": ["supplier.s_suppkey", "supplier.s_name", "supplier.s_address", "supplier.s_nationkey", "supplier.s_phone", "supplier.s_acctbal", "supplier.s_comment", "nation.n_nationkey", "nation.n_name", "nation.n_regionkey", "nation.n_comment"],
        "Inner Unique": False,
        "Join Filter": "(supplier.s_nationkey <> nation.n_nationkey)",
        "Rows Removed by Join Filter": 10000,
        "Plans": [
            {
                "Node Type": "Seq Scan",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Relation Name": "supplier",
                "Schema": "public",
                "Alias": "supplier",
                "Startup Cost": 0.00,
                "Total Cost": 322.00,
                "Plan Rows": 10000,
                "Plan Width": 144,
                "Actual Startup Time": 0.008,
                "Actual Total Time": 0.869,
                "Actual Rows": 10000,
                "Actual Loops": 1,
                "Output": ["supplier.s_suppkey", "supplier.s_name", "supplier.s_address", "supplier.s_nationkey", "supplier.s_phone", "supplier.s_acctbal", "supplier.s_comment"]
            },
            {
                "Node Type": "Materialize",
                "Parent Relationship": "Inner",
                "Parallel Aware": False,
                "Async Capable": False,
                "Startup Cost": 0.00,
                "Total Cost": 12.55,
                "Plan Rows": 170,
                "Plan Width": 434,
                "Actual Startup Time": 0.000,
                "Actual Total Time": 0.001,
                "Actual Rows": 25,
                "Actual Loops": 10000,
                "Output": ["nation.n_nationkey", "nation.n_name", "nation.n_regionkey", "nation.n_comment"],
                "Plans": [
                    {
                        "Node Type": "Seq Scan",
                        "Parent Relationship": "Outer",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Relation Name": "nation",
                        "Schema": "public",
                        "Alias": "nation",
                        "Startup Cost": 0.00,
                        "Total Cost": 11.70,
                        "Plan Rows": 170,
                        "Plan Width": 434,
                        "Actual Startup Time": 0.006,
                        "Actual Total Time": 0.008,
                        "Actual Rows": 25,
                        "Actual Loops": 1,
                        "Output": ["nation.n_nationkey", "nation.n_name", "nation.n_regionkey", "nation.n_comment"]
                    }
                ]
            }
        ]
    }
    QEP(op).resolve()
    assert_test(op)