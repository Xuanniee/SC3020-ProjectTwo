from explore import QEP
from utils import assert_test


def test_sort_and_limit():
    op = {
        "Node Type": "Limit",
        "Parallel Aware": False,
        "Async Capable": False,
        "Startup Cost": 41711.32,
        "Total Cost": 41860.74,
        "Plan Rows": 1,
        "Plan Width": 64,
        "Actual Startup Time": 1354.514,
        "Actual Total Time": 1360.062,
        "Actual Rows": 1,
        "Actual Loops": 1,
        "Output": ["(EXTRACT(year FROM orders.o_orderdate))", "((sum(CASE WHEN (n2.n_name = 'INDIA'::bpchar) THEN (lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)) ELSE '0'::numeric END) / sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))))"],
        "Plans": [
          {
            "Node Type": "Aggregate",
            "Strategy": "Sorted",
            "Partial Mode": "Simple",
            "Parent Relationship": "Outer",
            "Parallel Aware": False,
            "Async Capable": False,
            "Startup Cost": 41711.32,
            "Total Cost": 52171.09,
            "Plan Rows": 70,
            "Plan Width": 64,
            "Actual Startup Time": 1354.513,
            "Actual Total Time": 1360.060,
            "Actual Rows": 1,
            "Actual Loops": 1,
            "Output": ["(EXTRACT(year FROM orders.o_orderdate))", "(sum(CASE WHEN (n2.n_name = 'INDIA'::bpchar) THEN (lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)) ELSE '0'::numeric END) / sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount))))"],
            "Group Key": ["EXTRACT(year FROM orders.o_orderdate)"],
            "Plans": [
              {
                "Node Type": "Nested Loop",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Join Type": "Inner",
                "Startup Cost": 41711.32,
                "Total Cost": 52168.29,
                "Plan Rows": 70,
                "Plan Width": 148,
                "Actual Startup Time": 259.055,
                "Actual Total Time": 1357.224,
                "Actual Rows": 1314,
                "Actual Loops": 1,
                "Output": ["EXTRACT(year FROM orders.o_orderdate)", "n2.n_name", "lineitem.l_extendedprice", "lineitem.l_discount"],
                "Inner Unique": True,
                "Plans": [
                  {
                    "Node Type": "Nested Loop",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Join Type": "Inner",
                    "Startup Cost": 41711.17,
                    "Total Cost": 52156.40,
                    "Plan Rows": 70,
                    "Plan Width": 20,
                    "Actual Startup Time": 259.035,
                    "Actual Total Time": 1353.134,
                    "Actual Rows": 1314,
                    "Actual Loops": 1,
                    "Output": ["lineitem.l_extendedprice", "lineitem.l_discount", "supplier.s_nationkey", "orders.o_orderdate"],
                    "Inner Unique": True,
                    "Plans": [
                      {
                        "Node Type": "Nested Loop",
                        "Parent Relationship": "Outer",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Join Type": "Inner",
                        "Startup Cost": 41710.89,
                        "Total Cost": 52135.22,
                        "Plan Rows": 70,
                        "Plan Width": 20,
                        "Actual Startup Time": 259.026,
                        "Actual Total Time": 1344.450,
                        "Actual Rows": 1314,
                        "Actual Loops": 1,
                        "Output": ["lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_suppkey", "orders.o_orderdate"],
                        "Inner Unique": True,
                        "Plans": [
                          {
                            "Node Type": "Nested Loop",
                            "Parent Relationship": "Outer",
                            "Parallel Aware": False,
                            "Async Capable": False,
                            "Join Type": "Inner",
                            "Startup Cost": 41710.47,
                            "Total Cost": 47445.02,
                            "Plan Rows": 10585,
                            "Plan Width": 24,
                            "Actual Startup Time": 258.806,
                            "Actual Total Time": 743.739,
                            "Actual Rows": 183655,
                            "Actual Loops": 1,
                            "Output": ["lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_partkey", "lineitem.l_suppkey", "orders.o_orderdate"],
                            "Inner Unique": False,
                            "Plans": [
                              {
                                "Node Type": "Gather Merge",
                                "Parent Relationship": "Outer",
                                "Parallel Aware": False,
                                "Async Capable": False,
                                "Startup Cost": 41710.03,
                                "Total Cost": 42018.20,
                                "Plan Rows": 2646,
                                "Plan Width": 8,
                                "Actual Startup Time": 258.730,
                                "Actual Total Time": 282.449,
                                "Actual Rows": 45749,
                                "Actual Loops": 1,
                                "Output": ["orders.o_orderdate", "orders.o_orderkey"],
                                "Workers Planned": 2,
                                "Workers Launched": 2,
                                "Plans": [
                                  {
                                    "Node Type": "Sort",
                                    "Parent Relationship": "Outer",
                                    "Parallel Aware": False,
                                    "Async Capable": False,
                                    "Startup Cost": 40710.01,
                                    "Total Cost": 40712.77,
                                    "Plan Rows": 1102,
                                    "Plan Width": 8,
                                    "Actual Startup Time": 221.579,
                                    "Actual Total Time": 222.655,
                                    "Actual Rows": 16159,
                                    "Actual Loops": 3,
                                    "Output": ["orders.o_orderdate", "orders.o_orderkey", "(EXTRACT(year FROM orders.o_orderdate))"],
                                    "Sort Key": ["(EXTRACT(year FROM orders.o_orderdate))"],
                                    "Sort Method": "quicksort",
                                    "Sort Space Used": 2462,
                                    "Sort Space Type": "Memory",
                                    "Workers": [
                                      {
                                        "Worker Number": 0,
                                        "Actual Startup Time": 203.349,
                                        "Actual Total Time": 204.198,
                                        "Actual Rows": 16808,
                                        "Actual Loops": 1,
                                        "Sort Method": "quicksort",
                                        "Sort Space Used": 2446,
                                        "Sort Space Type": "Memory"
                                      },
                                      {
                                        "Worker Number": 1,
                                        "Actual Startup Time": 203.397,
                                        "Actual Total Time": 204.623,
                                        "Actual Rows": 16398,
                                        "Actual Loops": 1,
                                        "Sort Method": "quicksort",
                                        "Sort Space Used": 2413,
                                        "Sort Space Type": "Memory"
                                      }
                                    ],
                                    "Plans": [
                                      {
                                        "Node Type": "Hash Join",
                                        "Parent Relationship": "Outer",
                                        "Parallel Aware": True,
                                        "Async Capable": False,
                                        "Join Type": "Inner",
                                        "Startup Cost": 4476.96,
                                        "Total Cost": 40654.33,
                                        "Plan Rows": 1102,
                                        "Plan Width": 8,
                                        "Actual Startup Time": 26.188,
                                        "Actual Total Time": 209.127,
                                        "Actual Rows": 30569,
                                        "Actual Loops": 3,
                                        "Output": ["orders.o_orderdate", "orders.o_orderkey", "EXTRACT(year FROM orders.o_orderdate)"],
                                        "Inner Unique": False,
                                        "Hash Cond": "(orders.o_custkey = customer.c_custkey)",
                                        "Workers": [
                                          {
                                            "Worker Number": 0,
                                            "Actual Startup Time": 7.207,
                                            "Actual Total Time": 190.007,
                                            "Actual Rows": 30666,
                                            "Actual Loops": 1
                                          },
                                          {
                                            "Worker Number": 1,
                                            "Actual Startup Time": 7.618,
                                            "Actual Total Time": 190.209,
                                            "Actual Rows": 30067,
                                            "Actual Loops": 1
                                          }
                                        ],
                                        "Plans": [
                                          {
                                            "Node Type": "Seq Scan",
                                            "Parent Relationship": "Outer",
                                            "Parallel Aware": True,
                                            "Async Capable": False,
                                            "Relation Name": "orders",
                                            "Schema": "public",
                                            "Alias": "orders",
                                            "Startup Cost": 0.00,
                                            "Total Cost": 35470.00,
                                            "Plan Rows": 187404,
                                            "Plan Width": 12,
                                            "Actual Startup Time": 0.644,
                                            "Actual Total Time": 130.727,
                                            "Actual Rows": 152421,
                                            "Actual Loops": 3,
                                            "Output": ["orders.o_orderkey", "orders.o_custkey", "orders.o_orderstatus", "orders.o_totalprice", "orders.o_orderdate", "orders.o_orderpriority", "orders.o_clerk", "orders.o_shippriority", "orders.o_comment"],
                                            "Filter": "((orders.o_orderdate >= '1995-01-01'::date) AND (orders.o_orderdate <= '1996-12-31'::date))",
                                            "Rows Removed by Filter": 347579,
                                            "Workers": [
                                              {
                                                "Worker Number": 0,
                                                "Actual Startup Time": 0.737,
                                                "Actual Total Time": 130.916,
                                                "Actual Rows": 153539,
                                                "Actual Loops": 1
                                              },
                                              {
                                                "Worker Number": 1,
                                                "Actual Startup Time": 1.153,
                                                "Actual Total Time": 130.499,
                                                "Actual Rows": 149379,
                                                "Actual Loops": 1
                                              }
                                            ]
                                          },
                                          {
                                            "Node Type": "Hash",
                                            "Parent Relationship": "Inner",
                                            "Parallel Aware": True,
                                            "Async Capable": False,
                                            "Startup Cost": 4472.36,
                                            "Total Cost": 4472.36,
                                            "Plan Rows": 368,
                                            "Plan Width": 4,
                                            "Actual Startup Time": 23.474,
                                            "Actual Total Time": 23.479,
                                            "Actual Rows": 10061,
                                            "Actual Loops": 3,
                                            "Output": ["customer.c_custkey"],
                                            "Hash Buckets": 32768,
                                            "Original Hash Buckets": 1024,
                                            "Hash Batches": 1,
                                            "Original Hash Batches": 1,
                                            "Peak Memory Usage": 1752,
                                            "Workers": [
                                              {
                                                "Worker Number": 0,
                                                "Actual Startup Time": 3.444,
                                                "Actual Total Time": 3.449,
                                                "Actual Rows": 8,
                                                "Actual Loops": 1
                                              },
                                              {
                                                "Worker Number": 1,
                                                "Actual Startup Time": 3.374,
                                                "Actual Total Time": 3.380,
                                                "Actual Rows": 10,
                                                "Actual Loops": 1
                                              }
                                            ],
                                            "Plans": [
                                              {
                                                "Node Type": "Hash Join",
                                                "Parent Relationship": "Outer",
                                                "Parallel Aware": False,
                                                "Async Capable": False,
                                                "Join Type": "Inner",
                                                "Startup Cost": 24.31,
                                                "Total Cost": 4472.36,
                                                "Plan Rows": 368,
                                                "Plan Width": 4,
                                                "Actual Startup Time": 2.043,
                                                "Actual Total Time": 19.631,
                                                "Actual Rows": 10061,
                                                "Actual Loops": 3,
                                                "Output": ["customer.c_custkey"],
                                                "Inner Unique": False,
                                                "Hash Cond": "(customer.c_nationkey = n1.n_nationkey)",
                                                "Workers": [
                                                  {
                                                    "Worker Number": 0,
                                                    "Actual Startup Time": 2.833,
                                                    "Actual Total Time": 2.848,
                                                    "Actual Rows": 8,
                                                    "Actual Loops": 1
                                                  },
                                                  {
                                                    "Worker Number": 1,
                                                    "Actual Startup Time": 3.207,
                                                    "Actual Total Time": 3.231,
                                                    "Actual Rows": 10,
                                                    "Actual Loops": 1
                                                  }
                                                ],
                                                "Plans": [
                                                  {
                                                    "Node Type": "Seq Scan",
                                                    "Parent Relationship": "Outer",
                                                    "Parallel Aware": True,
                                                    "Async Capable": False,
                                                    "Relation Name": "customer",
                                                    "Schema": "public",
                                                    "Alias": "customer",
                                                    "Startup Cost": 0.00,
                                                    "Total Cost": 4210.00,
                                                    "Plan Rows": 62500,
                                                    "Plan Width": 8,
                                                    "Actual Startup Time": 0.987,
                                                    "Actual Total Time": 11.897,
                                                    "Actual Rows": 50000,
                                                    "Actual Loops": 3,
                                                    "Output": ["customer.c_custkey", "customer.c_name", "customer.c_address", "customer.c_nationkey", "customer.c_phone", "customer.c_acctbal", "customer.c_mktsegment", "customer.c_comment"],
                                                    "Workers": [
                                                      {
                                                        "Worker Number": 0,
                                                        "Actual Startup Time": 1.198,
                                                        "Actual Total Time": 1.201,
                                                        "Actual Rows": 41,
                                                        "Actual Loops": 1
                                                      },
                                                      {
                                                        "Worker Number": 1,
                                                        "Actual Startup Time": 1.733,
                                                        "Actual Total Time": 1.739,
                                                        "Actual Rows": 43,
                                                        "Actual Loops": 1
                                                      }
                                                    ]
                                                  },
                                                  {
                                                    "Node Type": "Hash",
                                                    "Parent Relationship": "Inner",
                                                    "Parallel Aware": False,
                                                    "Async Capable": False,
                                                    "Startup Cost": 24.29,
                                                    "Total Cost": 24.29,
                                                    "Plan Rows": 1,
                                                    "Plan Width": 4,
                                                    "Actual Startup Time": 1.039,
                                                    "Actual Total Time": 1.042,
                                                    "Actual Rows": 5,
                                                    "Actual Loops": 3,
                                                    "Output": ["n1.n_nationkey"],
                                                    "Hash Buckets": 1024,
                                                    "Original Hash Buckets": 1024,
                                                    "Hash Batches": 1,
                                                    "Original Hash Batches": 1,
                                                    "Peak Memory Usage": 9,
                                                    "Workers": [
                                                      {
                                                        "Worker Number": 0,
                                                        "Actual Startup Time": 1.616,
                                                        "Actual Total Time": 1.619,
                                                        "Actual Rows": 5,
                                                        "Actual Loops": 1
                                                      },
                                                      {
                                                        "Worker Number": 1,
                                                        "Actual Startup Time": 1.451,
                                                        "Actual Total Time": 1.454,
                                                        "Actual Rows": 5,
                                                        "Actual Loops": 1
                                                      }
                                                    ],
                                                    "Plans": [
                                                      {
                                                        "Node Type": "Hash Join",
                                                        "Parent Relationship": "Outer",
                                                        "Parallel Aware": False,
                                                        "Async Capable": False,
                                                        "Join Type": "Inner",
                                                        "Startup Cost": 12.14,
                                                        "Total Cost": 24.29,
                                                        "Plan Rows": 1,
                                                        "Plan Width": 4,
                                                        "Actual Startup Time": 1.027,
                                                        "Actual Total Time": 1.035,
                                                        "Actual Rows": 5,
                                                        "Actual Loops": 3,
                                                        "Output": ["n1.n_nationkey"],
                                                        "Inner Unique": True,
                                                        "Hash Cond": "(n1.n_regionkey = region.r_regionkey)",
                                                        "Workers": [
                                                          {
                                                            "Worker Number": 0,
                                                            "Actual Startup Time": 1.606,
                                                            "Actual Total Time": 1.613,
                                                            "Actual Rows": 5,
                                                            "Actual Loops": 1
                                                          },
                                                          {
                                                            "Worker Number": 1,
                                                            "Actual Startup Time": 1.432,
                                                            "Actual Total Time": 1.442,
                                                            "Actual Rows": 5,
                                                            "Actual Loops": 1
                                                          }
                                                        ],
                                                        "Plans": [
                                                          {
                                                            "Node Type": "Seq Scan",
                                                            "Parent Relationship": "Outer",
                                                            "Parallel Aware": False,
                                                            "Async Capable": False,
                                                            "Relation Name": "nation",
                                                            "Schema": "public",
                                                            "Alias": "n1",
                                                            "Startup Cost": 0.00,
                                                            "Total Cost": 11.70,
                                                            "Plan Rows": 170,
                                                            "Plan Width": 8,
                                                            "Actual Startup Time": 0.534,
                                                            "Actual Total Time": 0.536,
                                                            "Actual Rows": 25,
                                                            "Actual Loops": 3,
                                                            "Output": ["n1.n_nationkey", "n1.n_name", "n1.n_regionkey", "n1.n_comment"],
                                                            "Workers": [
                                                              {
                                                                "Worker Number": 0,
                                                                "Actual Startup Time": 0.889,
                                                                "Actual Total Time": 0.891,
                                                                "Actual Rows": 25,
                                                                "Actual Loops": 1
                                                              },
                                                              {
                                                                "Worker Number": 1,
                                                                "Actual Startup Time": 0.701,
                                                                "Actual Total Time": 0.705,
                                                                "Actual Rows": 25,
                                                                "Actual Loops": 1
                                                              }
                                                            ]
                                                          },
                                                          {
                                                            "Node Type": "Hash",
                                                            "Parent Relationship": "Inner",
                                                            "Parallel Aware": False,
                                                            "Async Capable": False,
                                                            "Startup Cost": 12.13,
                                                            "Total Cost": 12.13,
                                                            "Plan Rows": 1,
                                                            "Plan Width": 4,
                                                            "Actual Startup Time": 0.473,
                                                            "Actual Total Time": 0.474,
                                                            "Actual Rows": 1,
                                                            "Actual Loops": 3,
                                                            "Output": ["region.r_regionkey"],
                                                            "Hash Buckets": 1024,
                                                            "Original Hash Buckets": 1024,
                                                            "Hash Batches": 1,
                                                            "Original Hash Batches": 1,
                                                            "Peak Memory Usage": 9,
                                                            "Workers": [
                                                              {
                                                                "Worker Number": 0,
                                                                "Actual Startup Time": 0.687,
                                                                "Actual Total Time": 0.688,
                                                                "Actual Rows": 1,
                                                                "Actual Loops": 1
                                                              },
                                                              {
                                                                "Worker Number": 1,
                                                                "Actual Startup Time": 0.707,
                                                                "Actual Total Time": 0.708,
                                                                "Actual Rows": 1,
                                                                "Actual Loops": 1
                                                              }
                                                            ],
                                                            "Plans": [
                                                              {
                                                                "Node Type": "Seq Scan",
                                                                "Parent Relationship": "Outer",
                                                                "Parallel Aware": False,
                                                                "Async Capable": False,
                                                                "Relation Name": "region",
                                                                "Schema": "public",
                                                                "Alias": "region",
                                                                "Startup Cost": 0.00,
                                                                "Total Cost": 12.13,
                                                                "Plan Rows": 1,
                                                                "Plan Width": 4,
                                                                "Actual Startup Time": 0.460,
                                                                "Actual Total Time": 0.461,
                                                                "Actual Rows": 1,
                                                                "Actual Loops": 3,
                                                                "Output": ["region.r_regionkey"],
                                                                "Filter": "(region.r_name = 'ASIA'::bpchar)",
                                                                "Rows Removed by Filter": 4,
                                                                "Workers": [
                                                                  {
                                                                    "Worker Number": 0,
                                                                    "Actual Startup Time": 0.671,
                                                                    "Actual Total Time": 0.673,
                                                                    "Actual Rows": 1,
                                                                    "Actual Loops": 1
                                                                  },
                                                                  {
                                                                    "Worker Number": 1,
                                                                    "Actual Startup Time": 0.689,
                                                                    "Actual Total Time": 0.691,
                                                                    "Actual Rows": 1,
                                                                    "Actual Loops": 1
                                                                  }
                                                                ]
                                                              }
                                                            ]
                                                          }
                                                        ]
                                                      }
                                                    ]
                                                  }
                                                ]
                                              }
                                            ]
                                          }
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "Node Type": "Index Scan",
                                "Parent Relationship": "Inner",
                                "Parallel Aware": False,
                                "Async Capable": False,
                                "Scan Direction": "Forward",
                                "Index Name": "lineitem_pkey",
                                "Relation Name": "lineitem",
                                "Schema": "public",
                                "Alias": "lineitem",
                                "Startup Cost": 0.43,
                                "Total Cost": 1.90,
                                "Plan Rows": 15,
                                "Plan Width": 24,
                                "Actual Startup Time": 0.009,
                                "Actual Total Time": 0.009,
                                "Actual Rows": 4,
                                "Actual Loops": 45749,
                                "Output": ["lineitem.l_orderkey", "lineitem.l_partkey", "lineitem.l_suppkey", "lineitem.l_linenumber", "lineitem.l_quantity", "lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_tax", "lineitem.l_returnflag", "lineitem.l_linestatus", "lineitem.l_shipdate", "lineitem.l_commitdate", "lineitem.l_receiptdate", "lineitem.l_shipinstruct", "lineitem.l_shipmode", "lineitem.l_comment"],
                                "Index Cond": "(lineitem.l_orderkey = orders.o_orderkey)",
                                "Rows Removed by Index Recheck": 0
                              }
                            ]
                          },
                          {
                            "Node Type": "Index Scan",
                            "Parent Relationship": "Inner",
                            "Parallel Aware": False,
                            "Async Capable": False,
                            "Scan Direction": "Forward",
                            "Index Name": "part_pkey",
                            "Relation Name": "part",
                            "Schema": "public",
                            "Alias": "part",
                            "Startup Cost": 0.42,
                            "Total Cost": 0.44,
                            "Plan Rows": 1,
                            "Plan Width": 4,
                            "Actual Startup Time": 0.003,
                            "Actual Total Time": 0.003,
                            "Actual Rows": 0,
                            "Actual Loops": 183655,
                            "Output": ["part.p_partkey", "part.p_name", "part.p_mfgr", "part.p_brand", "part.p_type", "part.p_size", "part.p_container", "part.p_retailprice", "part.p_comment"],
                            "Index Cond": "(part.p_partkey = lineitem.l_partkey)",
                            "Rows Removed by Index Recheck": 0,
                            "Filter": "((part.p_type)::text = 'SMALL PLATED COPPER'::text)",
                            "Rows Removed by Filter": 1
                          }
                        ]
                      },
                      {
                        "Node Type": "Index Scan",
                        "Parent Relationship": "Inner",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Scan Direction": "Forward",
                        "Index Name": "supplier_pkey",
                        "Relation Name": "supplier",
                        "Schema": "public",
                        "Alias": "supplier",
                        "Startup Cost": 0.29,
                        "Total Cost": 0.30,
                        "Plan Rows": 1,
                        "Plan Width": 8,
                        "Actual Startup Time": 0.006,
                        "Actual Total Time": 0.006,
                        "Actual Rows": 1,
                        "Actual Loops": 1314,
                        "Output": ["supplier.s_suppkey", "supplier.s_name", "supplier.s_address", "supplier.s_nationkey", "supplier.s_phone", "supplier.s_acctbal", "supplier.s_comment"],
                        "Index Cond": "(supplier.s_suppkey = lineitem.l_suppkey)",
                        "Rows Removed by Index Recheck": 0
                      }
                    ]
                  },
                  {
                    "Node Type": "Index Scan",
                    "Parent Relationship": "Inner",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Scan Direction": "Forward",
                    "Index Name": "nation_pkey",
                    "Relation Name": "nation",
                    "Schema": "public",
                    "Alias": "n2",
                    "Startup Cost": 0.14,
                    "Total Cost": 0.17,
                    "Plan Rows": 1,
                    "Plan Width": 108,
                    "Actual Startup Time": 0.001,
                    "Actual Total Time": 0.001,
                    "Actual Rows": 1,
                    "Actual Loops": 1314,
                    "Output": ["n2.n_nationkey", "n2.n_name", "n2.n_regionkey", "n2.n_comment"],
                    "Index Cond": "(n2.n_nationkey = supplier.s_nationkey)",
                    "Rows Removed by Index Recheck": 0
                  }
                ]
              }
            ]
          }
        ]
      }
    QEP(op).resolve()
    assert_test(op)