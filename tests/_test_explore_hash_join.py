from explore import QEP
from utils import assert_test

def test_hash_join_seq_scan_nested_loop():
    op = {
        "Node Type": "Hash Join",
        "Parent Relationship": "Outer",
        "Parallel Aware": True,
        "Async Capable": False,
        "Join Type": "Inner",
        "Startup Cost": 12324.35,
        "Total Cost": 168586.06,
        "Plan Rows": 71,
        "Plan Width": 18,
        "Actual Startup Time": 44.891,
        "Actual Total Time": 1219.907,
        "Actual Rows": 106468,
        "Actual Loops": 3,
        "Output": ["lineitem.ctid", "lineitem.l_suppkey", "lineitem.l_orderkey", "partsupp.ps_suppkey"],
        "Inner Unique": False,
        "Hash Cond": "((lineitem.l_suppkey = partsupp.ps_suppkey) AND (lineitem.l_partkey = partsupp.ps_partkey))",
        "Workers": [
            {
                "Worker Number": 0,
                "Actual Startup Time": 32.478,
                "Actual Total Time": 1205.711,
                "Actual Rows": 106363,
                "Actual Loops": 1
            },
            {
                "Worker Number": 1,
                "Actual Startup Time": 26.346,
                "Actual Total Time": 1181.711,
                "Actual Rows": 103322,
                "Actual Loops": 1
            }
        ],
        "Plans": [
            {
                "Node Type": "Seq Scan",
                "Parent Relationship": "Outer",
                "Parallel Aware": True,
                "Async Capable": False,
                "Relation Name": "lineitem",
                "Schema": "public",
                "Alias": "lineitem",
                "Startup Cost": 0.00,
                "Total Cost": 137507.81,
                "Plan Rows": 2500481,
                "Plan Width": 18,
                "Actual Startup Time": 0.744,
                "Actual Total Time": 640.402,
                "Actual Rows": 2000405,
                "Actual Loops": 3,
                "Output": ["lineitem.ctid", "lineitem.l_suppkey", "lineitem.l_partkey", "lineitem.l_orderkey"],
                "Workers": [
                    {
                      "Worker Number": 0,
                      "Actual Startup Time": 1.307,
                      "Actual Total Time": 658.575,
                      "Actual Rows": 1996928,
                      "Actual Loops": 1
                    },
                    {
                      "Worker Number": 1,
                      "Actual Startup Time": 0.874,
                      "Actual Total Time": 625.935,
                      "Actual Rows": 1942256,
                      "Actual Loops": 1
                    }
                ]
            },
            {
                "Node Type": "Hash",
                "Parent Relationship": "Inner",
                "Parallel Aware": True,
                "Async Capable": False,
                "Startup Cost": 11970.83,
                "Total Cost": 11970.83,
                "Plan Rows": 23568,
                "Plan Width": 12,
                "Actual Startup Time": 43.957,
                "Actual Total Time": 43.959,
                "Actual Rows": 14219,
                "Actual Loops": 3,
                "Output": ["part.p_partkey", "partsupp.ps_suppkey", "partsupp.ps_partkey"],
                "Hash Buckets": 65536,
                "Original Hash Buckets": 65536,
                "Hash Batches": 1,
                "Original Hash Batches": 1,
                "Peak Memory Usage": 2560,
                "Workers": [
                    {
                      "Worker Number": 0,
                      "Actual Startup Time": 31.050,
                      "Actual Total Time": 31.052,
                      "Actual Rows": 8620,
                      "Actual Loops": 1
                    },
                    {
                      "Worker Number": 1,
                      "Actual Startup Time": 25.348,
                      "Actual Total Time": 25.351,
                      "Actual Rows": 6880,
                      "Actual Loops": 1
                    }
                ],
                "Plans": [
                    {
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
                ]
            }
        ]
    }
    QEP(op).resolve()
    assert_test(op)