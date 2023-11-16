from explore import QEP
from utils import assert_test


def test_aggregate_min():
    op = {
        "Node Type": "Aggregate",
        "Strategy": "Plain",
        "Partial Mode": "Finalize",
        "Parallel Aware": False,
        "Async Capable": False,
        "Startup Cost": 28572.32,
        "Total Cost": 28572.33,
        "Plan Rows": 1,
        "Plan Width": 32,
        "Actual Startup Time": 242.616,
        "Actual Total Time": 247.624,
        "Actual Rows": 1,
        "Actual Loops": 1,
        "Output": ["min(partsupp.ps_supplycost)"],
        "Shared Hit Blocks": 876,
        "Shared Read Blocks": 17249,
        "Shared Dirtied Blocks": 0,
        "Shared Written Blocks": 0,
        "Local Hit Blocks": 0,
        "Local Read Blocks": 0,
        "Local Dirtied Blocks": 0,
        "Local Written Blocks": 0,
        "Temp Read Blocks": 0,
        "Temp Written Blocks": 0,
        "Plans": [
            {
                "Node Type": "Gather",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Startup Cost": 28572.10,
                "Total Cost": 28572.31,
                "Plan Rows": 2,
                "Plan Width": 32,
                "Actual Startup Time": 241.632,
                "Actual Total Time": 247.614,
                "Actual Rows": 3,
                "Actual Loops": 1,
                "Output": ["(PARTIAL min(partsupp.ps_supplycost))"],
                "Workers Planned": 2,
                "Workers Launched": 2,
                "Single Copy": False,
                "Shared Hit Blocks": 876,
                "Shared Read Blocks": 17249,
                "Shared Dirtied Blocks": 0,
                "Shared Written Blocks": 0,
                "Local Hit Blocks": 0,
                "Local Read Blocks": 0,
                "Local Dirtied Blocks": 0,
                "Local Written Blocks": 0,
                "Temp Read Blocks": 0,
                "Temp Written Blocks": 0,
                "Plans": [
                    {
                        "Node Type": "Aggregate",
                        "Strategy": "Plain",
                        "Partial Mode": "Partial",
                        "Parent Relationship": "Outer",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Startup Cost": 27572.10,
                        "Total Cost": 27572.11,
                        "Plan Rows": 1,
                        "Plan Width": 32,
                        "Actual Startup Time": 213.630,
                        "Actual Total Time": 213.633,
                        "Actual Rows": 1,
                        "Actual Loops": 3,
                        "Output": ["PARTIAL min(partsupp.ps_supplycost)"],
                        "Shared Hit Blocks": 876,
                        "Shared Read Blocks": 17249,
                        "Shared Dirtied Blocks": 0,
                        "Shared Written Blocks": 0,
                        "Local Hit Blocks": 0,
                        "Local Read Blocks": 0,
                        "Local Dirtied Blocks": 0,
                        "Local Written Blocks": 0,
                        "Temp Read Blocks": 0,
                        "Temp Written Blocks": 0,
                        "Workers": [
                            {
                            "Worker Number": 0,
                            "Actual Startup Time": 197.624,
                            "Actual Total Time": 197.627,
                            "Actual Rows": 1,
                            "Actual Loops": 1,
                            "Shared Hit Blocks": 176,
                            "Shared Read Blocks": 5756,
                            "Shared Dirtied Blocks": 0,
                            "Shared Written Blocks": 0,
                            "Local Hit Blocks": 0,
                            "Local Read Blocks": 0,
                            "Local Dirtied Blocks": 0,
                            "Local Written Blocks": 0,
                            "Temp Read Blocks": 0,
                            "Temp Written Blocks": 0
                            },
                            {
                            "Worker Number": 1,
                            "Actual Startup Time": 202.153,
                            "Actual Total Time": 202.155,
                            "Actual Rows": 1,
                            "Actual Loops": 1,
                            "Shared Hit Blocks": 217,
                            "Shared Read Blocks": 5745,
                            "Shared Dirtied Blocks": 0,
                            "Shared Written Blocks": 0,
                            "Local Hit Blocks": 0,
                            "Local Read Blocks": 0,
                            "Local Dirtied Blocks": 0,
                            "Local Written Blocks": 0,
                            "Temp Read Blocks": 0,
                            "Temp Written Blocks": 0
                            }
                        ],
                        "Plans": [
                            {
                                "Node Type": "Hash Join",
                                "Parent Relationship": "Outer",
                                "Parallel Aware": True,
                                "Async Capable": False,
                                "Join Type": "Inner",
                                "Startup Cost": 5079.42,
                                "Total Cost": 26738.77,
                                "Plan Rows": 333333,
                                "Plan Width": 6,
                                "Actual Startup Time": 24.683,
                                "Actual Total Time": 175.100,
                                "Actual Rows": 266667,
                                "Actual Loops": 3,
                                "Output": ["partsupp.ps_supplycost"],
                                "Inner Unique": True,
                                "Hash Cond": "(partsupp.ps_partkey = part.p_partkey)",
                                "Shared Hit Blocks": 876,
                                "Shared Read Blocks": 17249,
                                "Shared Dirtied Blocks": 0,
                                "Shared Written Blocks": 0,
                                "Local Hit Blocks": 0,
                                "Local Read Blocks": 0,
                                "Local Dirtied Blocks": 0,
                                "Local Written Blocks": 0,
                                "Temp Read Blocks": 0,
                                "Temp Written Blocks": 0,
                                "Workers": [
                                    {
                                    "Worker Number": 0,
                                    "Actual Startup Time": 9.232,
                                    "Actual Total Time": 159.258,
                                    "Actual Rows": 266812,
                                    "Actual Loops": 1,
                                    "Shared Hit Blocks": 176,
                                    "Shared Read Blocks": 5756,
                                    "Shared Dirtied Blocks": 0,
                                    "Shared Written Blocks": 0,
                                    "Local Hit Blocks": 0,
                                    "Local Read Blocks": 0,
                                    "Local Dirtied Blocks": 0,
                                    "Local Written Blocks": 0,
                                    "Temp Read Blocks": 0,
                                    "Temp Written Blocks": 0
                                    },
                                    {
                                        "Worker Number": 1,
                                        "Actual Startup Time": 12.903,
                                        "Actual Total Time": 164.273,
                                        "Actual Rows": 266150,
                                        "Actual Loops": 1,
                                        "Shared Hit Blocks": 217,
                                        "Shared Read Blocks": 5745,
                                        "Shared Dirtied Blocks": 0,
                                        "Shared Written Blocks": 0,
                                        "Local Hit Blocks": 0,
                                        "Local Read Blocks": 0,
                                        "Local Dirtied Blocks": 0,
                                        "Local Written Blocks": 0,
                                        "Temp Read Blocks": 0,
                                        "Temp Written Blocks": 0
                                    }
                                ],
                                "Plans": [
                                    {
                                        "Node Type": "Seq Scan",
                                        "Parent Relationship": "Outer",
                                        "Parallel Aware": True,
                                        "Async Capable": False,
                                        "Relation Name": "partsupp",
                                        "Schema": "public",
                                        "Alias": "partsupp",
                                        "Startup Cost": 0.00,
                                        "Total Cost": 20784.33,
                                        "Plan Rows": 333333,
                                        "Plan Width": 10,
                                        "Actual Startup Time": 0.418,
                                        "Actual Total Time": 67.177,
                                        "Actual Rows": 266667,
                                        "Actual Loops": 3,
                                        "Output": ["partsupp.ps_partkey", "partsupp.ps_suppkey", "partsupp.ps_availqty", "partsupp.ps_supplycost", "partsupp.ps_comment"],
                                        "Shared Hit Blocks": 202,
                                        "Shared Read Blocks": 17249,
                                        "Shared Dirtied Blocks": 0,
                                        "Shared Written Blocks": 0,
                                        "Local Hit Blocks": 0,
                                        "Local Read Blocks": 0,
                                        "Local Dirtied Blocks": 0,
                                        "Local Written Blocks": 0,
                                        "Temp Read Blocks": 0,
                                        "Temp Written Blocks": 0,
                                        "Workers": [
                                            {
                                                "Worker Number": 0,
                                                "Actual Startup Time": 1.136,
                                                "Actual Total Time": 67.752,
                                                "Actual Rows": 266812,
                                                "Actual Loops": 1,
                                                "Shared Hit Blocks": 64,
                                                "Shared Read Blocks": 5756,
                                                "Shared Dirtied Blocks": 0,
                                                "Shared Written Blocks": 0,
                                                "Local Hit Blocks": 0,
                                                "Local Read Blocks": 0,
                                                "Local Dirtied Blocks": 0,
                                                "Local Written Blocks": 0,
                                                "Temp Read Blocks": 0,
                                                "Temp Written Blocks": 0
                                            },
                                            {
                                                "Worker Number": 1,
                                                "Actual Startup Time": 0.025,
                                                "Actual Total Time": 68.074,
                                                "Actual Rows": 266150,
                                                "Actual Loops": 1,
                                                "Shared Hit Blocks": 64,
                                                "Shared Read Blocks": 5745,
                                                "Shared Dirtied Blocks": 0,
                                                "Shared Written Blocks": 0,
                                                "Local Hit Blocks": 0,
                                                "Local Read Blocks": 0,
                                                "Local Dirtied Blocks": 0,
                                                "Local Written Blocks": 0,
                                                "Temp Read Blocks": 0,
                                                "Temp Written Blocks": 0
                                            }
                                        ]
                                    },
                                    {
                                        "Node Type": "Hash",
                                        "Parent Relationship": "Inner",
                                        "Parallel Aware": True,
                                        "Async Capable": False,
                                        "Startup Cost": 4037.75,
                                        "Total Cost": 4037.75,
                                        "Plan Rows": 83333,
                                        "Plan Width": 4,
                                        "Actual Startup Time": 23.837,
                                        "Actual Total Time": 23.838,
                                        "Actual Rows": 66667,
                                        "Actual Loops": 3,
                                        "Output": ["part.p_partkey"],
                                        "Hash Buckets": 262144,
                                        "Original Hash Buckets": 262144,
                                        "Hash Batches": 1,
                                        "Original Hash Batches": 1,
                                        "Peak Memory Usage": 9920,
                                        "Shared Hit Blocks": 552,
                                        "Shared Read Blocks": 0,
                                        "Shared Dirtied Blocks": 0,
                                        "Shared Written Blocks": 0,
                                        "Local Hit Blocks": 0,
                                        "Local Read Blocks": 0,
                                        "Local Dirtied Blocks": 0,
                                        "Local Written Blocks": 0,
                                        "Temp Read Blocks": 0,
                                        "Temp Written Blocks": 0,
                                        "Workers": [
                                            {
                                                "Worker Number": 0,
                                                "Actual Startup Time": 7.871,
                                                "Actual Total Time": 7.872,
                                                "Actual Rows": 18098,
                                                "Actual Loops": 1,
                                                "Shared Hit Blocks": 51,
                                                "Shared Read Blocks": 0,
                                                "Shared Dirtied Blocks": 0,
                                                "Shared Written Blocks": 0,
                                                "Local Hit Blocks": 0,
                                                "Local Read Blocks": 0,
                                                "Local Dirtied Blocks": 0,
                                                "Local Written Blocks": 0,
                                                "Temp Read Blocks": 0,
                                                "Temp Written Blocks": 0
                                            },
                                            {
                                                "Worker Number": 1,
                                                "Actual Startup Time": 12.672,
                                                "Actual Total Time": 12.672,
                                                "Actual Rows": 33306,
                                                "Actual Loops": 1,
                                                "Shared Hit Blocks": 92,
                                                "Shared Read Blocks": 0,
                                                "Shared Dirtied Blocks": 0,
                                                "Shared Written Blocks": 0,
                                                "Local Hit Blocks": 0,
                                                "Local Read Blocks": 0,
                                                "Local Dirtied Blocks": 0,
                                                "Local Written Blocks": 0,
                                                "Temp Read Blocks": 0,
                                                "Temp Written Blocks": 0
                                            }
                                        ],
                                        "Plans": [
                                            {
                                                "Node Type": "Index Only Scan",
                                                "Parent Relationship": "Outer",
                                                "Parallel Aware": True,
                                                "Async Capable": False,
                                                "Scan Direction": "Forward",
                                                "Index Name": "part_pkey",
                                                "Relation Name": "part",
                                                "Schema": "public",
                                                "Alias": "part",
                                                "Startup Cost": 0.42,
                                                "Total Cost": 4037.75,
                                                "Plan Rows": 83333,
                                                "Plan Width": 4,
                                                "Actual Startup Time": 0.540,
                                                "Actual Total Time": 7.874,
                                                "Actual Rows": 66667,
                                                "Actual Loops": 3,
                                                "Output": ["part.p_partkey"],
                                                "Heap Fetches": 0,
                                                "Shared Hit Blocks": 552,
                                                "Shared Read Blocks": 0,
                                                "Shared Dirtied Blocks": 0,
                                                "Shared Written Blocks": 0,
                                                "Local Hit Blocks": 0,
                                                "Local Read Blocks": 0,
                                                "Local Dirtied Blocks": 0,
                                                "Local Written Blocks": 0,
                                                "Temp Read Blocks": 0,
                                                "Temp Written Blocks": 0,
                                                "Workers": [
                                                    {
                                                    "Worker Number": 0,
                                                    "Actual Startup Time": 0.810,
                                                    "Actual Total Time": 3.006,
                                                    "Actual Rows": 18098,
                                                    "Actual Loops": 1,
                                                    "Shared Hit Blocks": 51,
                                                    "Shared Read Blocks": 0,
                                                    "Shared Dirtied Blocks": 0,
                                                    "Shared Written Blocks": 0,
                                                    "Local Hit Blocks": 0,
                                                    "Local Read Blocks": 0,
                                                    "Local Dirtied Blocks": 0,
                                                    "Local Written Blocks": 0,
                                                    "Temp Read Blocks": 0,
                                                    "Temp Written Blocks": 0
                                                    },
                                                    {
                                                    "Worker Number": 1,
                                                    "Actual Startup Time": 0.783,
                                                    "Actual Total Time": 4.827,
                                                    "Actual Rows": 33306,
                                                    "Actual Loops": 1,
                                                    "Shared Hit Blocks": 92,
                                                    "Shared Read Blocks": 0,
                                                    "Shared Dirtied Blocks": 0,
                                                    "Shared Written Blocks": 0,
                                                    "Local Hit Blocks": 0,
                                                    "Local Read Blocks": 0,
                                                    "Local Dirtied Blocks": 0,
                                                    "Local Written Blocks": 0,
                                                    "Temp Read Blocks": 0,
                                                    "Temp Written Blocks": 0
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
    QEP(op).resolve()
    assert_test(op)


def test_aggregate_multi_brackets():
    op = {
      "Node Type": "Sort",
      "Parallel Aware": False,
      "Async Capable": False,
      "Startup Cost": 224299.41,
      "Total Cost": 225079.07,
      "Plan Rows": 311864,
      "Plan Width": 44,
      "Actual Startup Time": 1050.079,
      "Actual Total Time": 1058.375,
      "Actual Rows": 11291,
      "Actual Loops": 1,
      "Output": ["lineitem.l_orderkey", "(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount))))", "orders.o_orderdate", "orders.o_shippriority"],
      "Sort Key": ["(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))) DESC", "orders.o_orderdate"],
      "Sort Method": "quicksort",
      "Sort Space Used": 1090,
      "Sort Space Type": "Memory",
      "Plans": [
        {
          "Node Type": "Aggregate",
          "Strategy": "Sorted",
          "Partial Mode": "Finalize",
          "Parent Relationship": "Outer",
          "Parallel Aware": False,
          "Async Capable": False,
          "Startup Cost": 145204.99,
          "Total Cost": 186247.45,
          "Plan Rows": 311864,
          "Plan Width": 44,
          "Actual Startup Time": 1027.136,
          "Actual Total Time": 1053.062,
          "Actual Rows": 11291,
          "Actual Loops": 1,
          "Output": ["lineitem.l_orderkey", "sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))", "orders.o_orderdate", "orders.o_shippriority"],
          "Group Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
          "Plans": [
            {
              "Node Type": "Gather Merge",
              "Parent Relationship": "Outer",
              "Parallel Aware": False,
              "Async Capable": False,
              "Startup Cost": 145204.99,
              "Total Cost": 179100.57,
              "Plan Rows": 259886,
              "Plan Width": 44,
              "Actual Startup Time": 1027.122,
              "Actual Total Time": 1043.626,
              "Actual Rows": 11291,
              "Actual Loops": 1,
              "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "(PARTIAL sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount))))"],
              "Workers Planned": 2,
              "Workers Launched": 2,
              "Plans": [
                {
                  "Node Type": "Aggregate",
                  "Strategy": "Sorted",
                  "Partial Mode": "Partial",
                  "Parent Relationship": "Outer",
                  "Parallel Aware": False,
                  "Async Capable": False,
                  "Startup Cost": 144204.97,
                  "Total Cost": 148103.26,
                  "Plan Rows": 129943,
                  "Plan Width": 44,
                  "Actual Startup Time": 978.483,
                  "Actual Total Time": 986.203,
                  "Actual Rows": 3764,
                  "Actual Loops": 3,
                  "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "PARTIAL sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))"],
                  "Group Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
                  "Workers": [
                    {
                      "Worker Number": 0,
                      "Actual Startup Time": 954.512,
                      "Actual Total Time": 962.961,
                      "Actual Rows": 4243,
                      "Actual Loops": 1
                    },
                    {
                      "Worker Number": 1,
                      "Actual Startup Time": 954.872,
                      "Actual Total Time": 961.884,
                      "Actual Rows": 3320,
                      "Actual Loops": 1
                    }
                  ],
                  "Plans": [
                    {
                      "Node Type": "Sort",
                      "Parent Relationship": "Outer",
                      "Parallel Aware": False,
                      "Async Capable": False,
                      "Startup Cost": 144204.97,
                      "Total Cost": 144529.82,
                      "Plan Rows": 129943,
                      "Plan Width": 24,
                      "Actual Startup Time": 978.468,
                      "Actual Total Time": 978.914,
                      "Actual Rows": 9939,
                      "Actual Loops": 3,
                      "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "lineitem.l_extendedprice", "lineitem.l_discount"],
                      "Sort Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
                      "Sort Method": "quicksort",
                      "Sort Space Used": 1066,
                      "Sort Space Type": "Memory",
                      "Workers": [
                        {
                          "Worker Number": 0,
                          "Actual Startup Time": 954.498,
                          "Actual Total Time": 955.026,
                          "Actual Rows": 11149,
                          "Actual Loops": 1,
                          "Sort Method": "quicksort",
                          "Sort Space Used": 1147,
                          "Sort Space Type": "Memory"
                        },
                        {
                          "Worker Number": 1,
                          "Actual Startup Time": 954.852,
                          "Actual Total Time": 955.234,
                          "Actual Rows": 8696,
                          "Actual Loops": 1,
                          "Sort Method": "quicksort",
                          "Sort Space Used": 979,
                          "Sort Space Type": "Memory"
                        }
                      ],
                      "Plans": [
                        {
                          "Node Type": "Nested Loop",
                          "Parent Relationship": "Outer",
                          "Parallel Aware": False,
                          "Async Capable": False,
                          "Join Type": "Inner",
                          "Startup Cost": 4521.03,
                          "Total Cost": 130500.92,
                          "Plan Rows": 129943,
                          "Plan Width": 24,
                          "Actual Startup Time": 20.416,
                          "Actual Total Time": 973.025,
                          "Actual Rows": 9939,
                          "Actual Loops": 3,
                          "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "lineitem.l_extendedprice", "lineitem.l_discount"],
                          "Inner Unique": False,
                          "Workers": [
                            {
                              "Worker Number": 0,
                              "Actual Startup Time": 3.420,
                              "Actual Total Time": 948.879,
                              "Actual Rows": 11149,
                              "Actual Loops": 1
                            },
                            {
                              "Worker Number": 1,
                              "Actual Startup Time": 3.059,
                              "Actual Total Time": 949.692,
                              "Actual Rows": 8696,
                              "Actual Loops": 1
                            }
                          ],
                          "Plans": [
                            {
                              "Node Type": "Hash Join",
                              "Parent Relationship": "Outer",
                              "Parallel Aware": True,
                              "Async Capable": False,
                              "Join Type": "Inner",
                              "Startup Cost": 4520.60,
                              "Total Cost": 39182.00,
                              "Plan Rows": 56740,
                              "Plan Width": 12,
                              "Actual Startup Time": 18.978,
                              "Actual Total Time": 287.464,
                              "Actual Rows": 45331,
                              "Actual Loops": 3,
                              "Output": ["orders.o_orderdate", "orders.o_shippriority", "orders.o_orderkey"],
                              "Inner Unique": True,
                              "Hash Cond": "(orders.o_custkey = customer.c_custkey)",
                              "Workers": [
                                {
                                  "Worker Number": 0,
                                  "Actual Startup Time": 1.405,
                                  "Actual Total Time": 299.500,
                                  "Actual Rows": 51247,
                                  "Actual Loops": 1
                                },
                                {
                                  "Worker Number": 1,
                                  "Actual Startup Time": 0.986,
                                  "Actual Total Time": 229.804,
                                  "Actual Rows": 39712,
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
                                  "Total Cost": 33907.50,
                                  "Plan Rows": 287193,
                                  "Plan Width": 16,
                                  "Actual Startup Time": 0.711,
                                  "Actual Total Time": 170.094,
                                  "Actual Rows": 227110,
                                  "Actual Loops": 3,
                                  "Output": ["orders.o_orderkey", "orders.o_custkey", "orders.o_orderstatus", "orders.o_totalprice", "orders.o_orderdate", "orders.o_orderpriority", "orders.o_clerk", "orders.o_shippriority", "orders.o_comment"],
                                  "Filter": "(orders.o_orderdate < '1995-01-01'::date)",
                                  "Rows Removed by Filter": 272890,
                                  "Workers": [
                                    {
                                      "Worker Number": 0,
                                      "Actual Startup Time": 1.249,
                                      "Actual Total Time": 189.202,
                                      "Actual Rows": 255827,
                                      "Actual Loops": 1
                                    },
                                    {
                                      "Worker Number": 1,
                                      "Actual Startup Time": 0.865,
                                      "Actual Total Time": 139.116,
                                      "Actual Rows": 199416,
                                      "Actual Loops": 1
                                    }
                                  ]
                                },
                                {
                                  "Node Type": "Hash",
                                  "Parent Relationship": "Inner",
                                  "Parallel Aware": True,
                                  "Async Capable": False,
                                  "Startup Cost": 4366.25,
                                  "Total Cost": 4366.25,
                                  "Plan Rows": 12348,
                                  "Plan Width": 4,
                                  "Actual Startup Time": 18.141,
                                  "Actual Total Time": 18.142,
                                  "Actual Rows": 10063,
                                  "Actual Loops": 3,
                                  "Output": ["customer.c_custkey"],
                                  "Hash Buckets": 32768,
                                  "Original Hash Buckets": 32768,
                                  "Hash Batches": 1,
                                  "Original Hash Batches": 1,
                                  "Peak Memory Usage": 1440,
                                  "Workers": [
                                    {
                                      "Worker Number": 0,
                                      "Actual Startup Time": 0.031,
                                      "Actual Total Time": 0.033,
                                      "Actual Rows": 0,
                                      "Actual Loops": 1
                                    },
                                    {
                                      "Worker Number": 1,
                                      "Actual Startup Time": 0.035,
                                      "Actual Total Time": 0.036,
                                      "Actual Rows": 0,
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
                                      "Total Cost": 4366.25,
                                      "Plan Rows": 12348,
                                      "Plan Width": 4,
                                      "Actual Startup Time": 0.037,
                                      "Actual Total Time": 46.606,
                                      "Actual Rows": 30189,
                                      "Actual Loops": 1,
                                      "Output": ["customer.c_custkey"],
                                      "Filter": "(customer.c_mktsegment = 'HOUSEHOLD'::bpchar)",
                                      "Rows Removed by Filter": 119811,
                                      "Workers": [
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
                              "Total Cost": 1.52,
                              "Plan Rows": 9,
                              "Plan Width": 16,
                              "Actual Startup Time": 0.015,
                              "Actual Total Time": 0.015,
                              "Actual Rows": 0,
                              "Actual Loops": 135994,
                              "Output": ["lineitem.l_orderkey", "lineitem.l_partkey", "lineitem.l_suppkey", "lineitem.l_linenumber", "lineitem.l_quantity", "lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_tax", "lineitem.l_returnflag", "lineitem.l_linestatus", "lineitem.l_shipdate", "lineitem.l_commitdate", "lineitem.l_receiptdate", "lineitem.l_shipinstruct", "lineitem.l_shipmode", "lineitem.l_comment"],
                              "Index Cond": "(lineitem.l_orderkey = orders.o_orderkey)",
                              "Rows Removed by Index Recheck": 0,
                              "Filter": "(lineitem.l_shipdate > '1995-01-01'::date)",
                              "Rows Removed by Filter": 4,
                              "Workers": [
                                {
                                  "Worker Number": 0,
                                  "Actual Startup Time": 0.012,
                                  "Actual Total Time": 0.012,
                                  "Actual Rows": 0,
                                  "Actual Loops": 51247
                                },
                                {
                                  "Worker Number": 1,
                                  "Actual Startup Time": 0.018,
                                  "Actual Total Time": 0.018,
                                  "Actual Rows": 0,
                                  "Actual Loops": 39712
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
    QEP(op).resolve()
    assert_test(op)