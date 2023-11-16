from explore import QEP
from utils import assert_test


def _test_general_1():
    op = {
        "Node Type": "Limit",
        "Parallel Aware": False,
        "Async Capable": False,
        "Startup Cost": 232267.44,
        "Total Cost": 232267.76,
        "Plan Rows": 1,
        "Plan Width": 236,
        "Actual Startup Time": 3482.426,
        "Actual Total Time": 3489.403,
        "Actual Rows": 1,
        "Actual Loops": 1,
        "Output": ["l_returnflag", "l_linestatus", "(sum(l_quantity))", "(sum(l_extendedprice))", "(sum((l_extendedprice * ('1'::numeric - l_discount))))", "(sum(((l_extendedprice * ('1'::numeric - l_discount)) * ('1'::numeric + l_tax))))", "(avg(l_quantity))", "(avg(l_extendedprice))", "(avg(l_discount))", "(count(*))"],
        "Plans": [
          {
            "Node Type": "Aggregate",
            "Strategy": "Sorted",
            "Partial Mode": "Finalize",
            "Parent Relationship": "Outer",
            "Parallel Aware": False,
            "Async Capable": False,
            "Startup Cost": 232267.44,
            "Total Cost": 232269.39,
            "Plan Rows": 6,
            "Plan Width": 236,
            "Actual Startup Time": 3482.425,
            "Actual Total Time": 3489.401,
            "Actual Rows": 1,
            "Actual Loops": 1,
            "Output": ["l_returnflag", "l_linestatus", "sum(l_quantity)", "sum(l_extendedprice)", "sum((l_extendedprice * ('1'::numeric - l_discount)))", "sum(((l_extendedprice * ('1'::numeric - l_discount)) * ('1'::numeric + l_tax)))", "avg(l_quantity)", "avg(l_extendedprice)", "avg(l_discount)", "count(*)"],
            "Group Key": ["lineitem.l_returnflag", "lineitem.l_linestatus"],
            "Plans": [
              {
                "Node Type": "Gather Merge",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Startup Cost": 232267.44,
                "Total Cost": 232268.84,
                "Plan Rows": 12,
                "Plan Width": 236,
                "Actual Startup Time": 3482.378,
                "Actual Total Time": 3489.362,
                "Actual Rows": 4,
                "Actual Loops": 1,
                "Output": ["l_returnflag", "l_linestatus", "(PARTIAL sum(l_quantity))", "(PARTIAL sum(l_extendedprice))", "(PARTIAL sum((l_extendedprice * ('1'::numeric - l_discount))))", "(PARTIAL sum(((l_extendedprice * ('1'::numeric - l_discount)) * ('1'::numeric + l_tax))))", "(PARTIAL avg(l_quantity))", "(PARTIAL avg(l_extendedprice))", "(PARTIAL avg(l_discount))", "(PARTIAL count(*))"],
                "Workers Planned": 2,
                "Workers Launched": 2,
                "Plans": [
                  {
                    "Node Type": "Sort",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Startup Cost": 231267.41,
                    "Total Cost": 231267.43,
                    "Plan Rows": 6,
                    "Plan Width": 236,
                    "Actual Startup Time": 3453.409,
                    "Actual Total Time": 3453.410,
                    "Actual Rows": 3,
                    "Actual Loops": 3,
                    "Output": ["l_returnflag", "l_linestatus", "(PARTIAL sum(l_quantity))", "(PARTIAL sum(l_extendedprice))", "(PARTIAL sum((l_extendedprice * ('1'::numeric - l_discount))))", "(PARTIAL sum(((l_extendedprice * ('1'::numeric - l_discount)) * ('1'::numeric + l_tax))))", "(PARTIAL avg(l_quantity))", "(PARTIAL avg(l_extendedprice))", "(PARTIAL avg(l_discount))", "(PARTIAL count(*))"],
                    "Sort Key": ["lineitem.l_returnflag", "lineitem.l_linestatus"],
                    "Sort Method": "quicksort",
                    "Sort Space Used": 27,
                    "Sort Space Type": "Memory",
                    "Workers": [
                      {
                        "Worker Number": 0,
                        "Actual Startup Time": 3438.829,
                        "Actual Total Time": 3438.830,
                        "Actual Rows": 4,
                        "Actual Loops": 1,
                        "Sort Method": "quicksort",
                        "Sort Space Used": 27,
                        "Sort Space Type": "Memory"
                      },
                      {
                        "Worker Number": 1,
                        "Actual Startup Time": 3439.538,
                        "Actual Total Time": 3439.540,
                        "Actual Rows": 4,
                        "Actual Loops": 1,
                        "Sort Method": "quicksort",
                        "Sort Space Used": 27,
                        "Sort Space Type": "Memory"
                      }
                    ],
                    "Plans": [
                      {
                        "Node Type": "Aggregate",
                        "Strategy": "Hashed",
                        "Partial Mode": "Partial",
                        "Parent Relationship": "Outer",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Startup Cost": 231267.20,
                        "Total Cost": 231267.34,
                        "Plan Rows": 6,
                        "Plan Width": 236,
                        "Actual Startup Time": 3453.292,
                        "Actual Total Time": 3453.300,
                        "Actual Rows": 4,
                        "Actual Loops": 3,
                        "Output": ["l_returnflag", "l_linestatus", "PARTIAL sum(l_quantity)", "PARTIAL sum(l_extendedprice)", "PARTIAL sum((l_extendedprice * ('1'::numeric - l_discount)))", "PARTIAL sum(((l_extendedprice * ('1'::numeric - l_discount)) * ('1'::numeric + l_tax)))", "PARTIAL avg(l_quantity)", "PARTIAL avg(l_extendedprice)", "PARTIAL avg(l_discount)", "PARTIAL count(*)"],
                        "Group Key": ["lineitem.l_returnflag", "lineitem.l_linestatus"],
                        "Planned Partitions": 0,
                        "HashAgg Batches": 1,
                        "Peak Memory Usage": 32,
                        "Disk Usage": 0,
                        "Workers": [
                          {
                            "Worker Number": 0,
                            "Actual Startup Time": 3438.634,
                            "Actual Total Time": 3438.640,
                            "Actual Rows": 4,
                            "Actual Loops": 1,
                            "HashAgg Batches": 1,
                            "Peak Memory Usage": 32,
                            "Disk Usage": 0
                          },
                          {
                            "Worker Number": 1,
                            "Actual Startup Time": 3439.433,
                            "Actual Total Time": 3439.439,
                            "Actual Rows": 4,
                            "Actual Loops": 1,
                            "HashAgg Batches": 1,
                            "Peak Memory Usage": 32,
                            "Disk Usage": 0
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
                            "Total Cost": 143759.01,
                            "Plan Rows": 2500234,
                            "Plan Width": 25,
                            "Actual Startup Time": 0.656,
                            "Actual Total Time": 606.600,
                            "Actual Rows": 2000310,
                            "Actual Loops": 3,
                            "Output": ["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity", "l_extendedprice", "l_discount", "l_tax", "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate", "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment"],
                            "Filter": "(lineitem.l_shipdate <= '1998-11-26 00:00:00'::timestamp without time zone)",
                            "Rows Removed by Filter": 95,
                            "Workers": [
                              {
                                "Worker Number": 0,
                                "Actual Startup Time": 1.155,
                                "Actual Total Time": 607.238,
                                "Actual Rows": 1958647,
                                "Actual Loops": 1
                              },
                              {
                                "Worker Number": 1,
                                "Actual Startup Time": 0.760,
                                "Actual Total Time": 606.712,
                                "Actual Rows": 1998066,
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

    QEP(op).resolve()
    assert_test(op)


def _test_general_2():
    op = {
        "Node Type": "Limit",
        "Parallel Aware": False,
        "Async Capable": False,
        "Startup Cost": 206686.55,
        "Total Cost": 206686.57,
        "Plan Rows": 10,
        "Plan Width": 44,
        "Actual Startup Time": 894.774,
        "Actual Total Time": 904.537,
        "Actual Rows": 10,
        "Actual Loops": 1,
        "Output": ["lineitem.l_orderkey", "(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount))))", "orders.o_orderdate", "orders.o_shippriority"],
        "Plans": [
          {
            "Node Type": "Sort",
            "Parent Relationship": "Outer",
            "Parallel Aware": False,
            "Async Capable": False,
            "Startup Cost": 206686.55,
            "Total Cost": 207462.94,
            "Plan Rows": 310556,
            "Plan Width": 44,
            "Actual Startup Time": 894.772,
            "Actual Total Time": 904.533,
            "Actual Rows": 10,
            "Actual Loops": 1,
            "Output": ["lineitem.l_orderkey", "(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount))))", "orders.o_orderdate", "orders.o_shippriority"],
            "Sort Key": ["(sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))) DESC", "orders.o_orderdate"],
            "Sort Method": "top-N heapsort",
            "Sort Space Used": 26,
            "Sort Space Type": "Memory",
            "Plans": [
              {
                "Node Type": "Aggregate",
                "Strategy": "Sorted",
                "Partial Mode": "Finalize",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Startup Cost": 159105.22,
                "Total Cost": 199975.54,
                "Plan Rows": 310556,
                "Plan Width": 44,
                "Actual Startup Time": 873.799,
                "Actual Total Time": 902.096,
                "Actual Rows": 11373,
                "Actual Loops": 1,
                "Output": ["lineitem.l_orderkey", "sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))", "orders.o_orderdate", "orders.o_shippriority"],
                "Group Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
                "Plans": [
                  {
                    "Node Type": "Gather Merge",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Startup Cost": 159105.22,
                    "Total Cost": 192858.64,
                    "Plan Rows": 258796,
                    "Plan Width": 44,
                    "Actual Startup Time": 873.788,
                    "Actual Total Time": 893.281,
                    "Actual Rows": 11373,
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
                        "Startup Cost": 158105.20,
                        "Total Cost": 161987.14,
                        "Plan Rows": 129398,
                        "Plan Width": 44,
                        "Actual Startup Time": 812.307,
                        "Actual Total Time": 819.697,
                        "Actual Rows": 3791,
                        "Actual Loops": 3,
                        "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "PARTIAL sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))"],
                        "Group Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
                        "Workers": [
                          {
                            "Worker Number": 0,
                            "Actual Startup Time": 781.939,
                            "Actual Total Time": 788.896,
                            "Actual Rows": 3604,
                            "Actual Loops": 1
                          },
                          {
                            "Worker Number": 1,
                            "Actual Startup Time": 782.144,
                            "Actual Total Time": 789.184,
                            "Actual Rows": 3494,
                            "Actual Loops": 1
                          }
                        ],
                        "Plans": [
                          {
                            "Node Type": "Sort",
                            "Parent Relationship": "Outer",
                            "Parallel Aware": False,
                            "Async Capable": False,
                            "Startup Cost": 158105.20,
                            "Total Cost": 158428.69,
                            "Plan Rows": 129398,
                            "Plan Width": 24,
                            "Actual Startup Time": 812.292,
                            "Actual Total Time": 812.698,
                            "Actual Rows": 10029,
                            "Actual Loops": 3,
                            "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "lineitem.l_extendedprice", "lineitem.l_discount"],
                            "Sort Key": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority"],
                            "Sort Method": "quicksort",
                            "Sort Space Used": 1155,
                            "Sort Space Type": "Memory",
                            "Workers": [
                              {
                                "Worker Number": 0,
                                "Actual Startup Time": 781.923,
                                "Actual Total Time": 782.319,
                                "Actual Rows": 9589,
                                "Actual Loops": 1,
                                "Sort Method": "quicksort",
                                "Sort Space Used": 1041,
                                "Sort Space Type": "Memory"
                              },
                              {
                                "Worker Number": 1,
                                "Actual Startup Time": 782.126,
                                "Actual Total Time": 782.507,
                                "Actual Rows": 9242,
                                "Actual Loops": 1,
                                "Sort Method": "quicksort",
                                "Sort Space Used": 1016,
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
                                "Startup Cost": 4523.03,
                                "Total Cost": 144461.87,
                                "Plan Rows": 129398,
                                "Plan Width": 24,
                                "Actual Startup Time": 20.311,
                                "Actual Total Time": 806.535,
                                "Actual Rows": 10029,
                                "Actual Loops": 3,
                                "Output": ["lineitem.l_orderkey", "orders.o_orderdate", "orders.o_shippriority", "lineitem.l_extendedprice", "lineitem.l_discount"],
                                "Inner Unique": False,
                                "Workers": [
                                  {
                                    "Worker Number": 0,
                                    "Actual Startup Time": 3.206,
                                    "Actual Total Time": 775.976,
                                    "Actual Rows": 9589,
                                    "Actual Loops": 1
                                  },
                                  {
                                    "Worker Number": 1,
                                    "Actual Startup Time": 4.819,
                                    "Actual Total Time": 775.934,
                                    "Actual Rows": 9242,
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
                                    "Startup Cost": 4522.60,
                                    "Total Cost": 39420.04,
                                    "Plan Rows": 75472,
                                    "Plan Width": 12,
                                    "Actual Startup Time": 18.717,
                                    "Actual Total Time": 258.201,
                                    "Actual Rows": 60511,
                                    "Actual Loops": 3,
                                    "Output": ["orders.o_orderdate", "orders.o_shippriority", "orders.o_orderkey"],
                                    "Inner Unique": True,
                                    "Hash Cond": "(orders.o_custkey = customer.c_custkey)",
                                    "Workers": [
                                      {
                                        "Worker Number": 0,
                                        "Actual Startup Time": 1.409,
                                        "Actual Total Time": 232.457,
                                        "Actual Rows": 58320,
                                        "Actual Loops": 1
                                      },
                                      {
                                        "Worker Number": 1,
                                        "Actual Startup Time": 1.872,
                                        "Actual Total Time": 228.365,
                                        "Actual Rows": 55940,
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
                                        "Plan Rows": 377108,
                                        "Plan Width": 16,
                                        "Actual Startup Time": 0.811,
                                        "Actual Total Time": 132.391,
                                        "Actual Rows": 299175,
                                        "Actual Loops": 3,
                                        "Output": ["orders.o_orderkey", "orders.o_custkey", "orders.o_orderstatus", "orders.o_totalprice", "orders.o_orderdate", "orders.o_orderpriority", "orders.o_clerk", "orders.o_shippriority", "orders.o_comment"],
                                        "Filter": "(orders.o_orderdate < '1995-12-12'::date)",
                                        "Rows Removed by Filter": 200825,
                                        "Workers": [
                                          {
                                            "Worker Number": 0,
                                            "Actual Startup Time": 0.945,
                                            "Actual Total Time": 128.638,
                                            "Actual Rows": 288373,
                                            "Actual Loops": 1
                                          },
                                          {
                                            "Worker Number": 1,
                                            "Actual Startup Time": 1.472,
                                            "Actual Total Time": 125.630,
                                            "Actual Rows": 276016,
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
                                        "Plan Rows": 12508,
                                        "Plan Width": 4,
                                        "Actual Startup Time": 17.581,
                                        "Actual Total Time": 17.581,
                                        "Actual Rows": 10047,
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
                                            "Actual Startup Time": 0.030,
                                            "Actual Total Time": 0.031,
                                            "Actual Rows": 0,
                                            "Actual Loops": 1
                                          },
                                          {
                                            "Worker Number": 1,
                                            "Actual Startup Time": 0.042,
                                            "Actual Total Time": 0.043,
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
                                            "Plan Rows": 12508,
                                            "Plan Width": 4,
                                            "Actual Startup Time": 0.023,
                                            "Actual Total Time": 44.963,
                                            "Actual Rows": 30142,
                                            "Actual Loops": 1,
                                            "Output": ["customer.c_custkey"],
                                            "Filter": "(customer.c_mktsegment = 'BUILDING'::bpchar)",
                                            "Rows Removed by Filter": 119858,
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
                                    "Total Cost": 1.33,
                                    "Plan Rows": 6,
                                    "Plan Width": 16,
                                    "Actual Startup Time": 0.009,
                                    "Actual Total Time": 0.009,
                                    "Actual Rows": 0,
                                    "Actual Loops": 181534,
                                    "Output": ["lineitem.l_orderkey", "lineitem.l_partkey", "lineitem.l_suppkey", "lineitem.l_linenumber", "lineitem.l_quantity", "lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_tax", "lineitem.l_returnflag", "lineitem.l_linestatus", "lineitem.l_shipdate", "lineitem.l_commitdate", "lineitem.l_receiptdate", "lineitem.l_shipinstruct", "lineitem.l_shipmode", "lineitem.l_comment"],
                                    "Index Cond": "(lineitem.l_orderkey = orders.o_orderkey)",
                                    "Rows Removed by Index Recheck": 0,
                                    "Filter": "(lineitem.l_shipdate > '1995-12-12'::date)",
                                    "Rows Removed by Filter": 4,
                                    "Workers": [
                                      {
                                        "Worker Number": 0,
                                        "Actual Startup Time": 0.009,
                                        "Actual Total Time": 0.009,
                                        "Actual Rows": 0,
                                        "Actual Loops": 58320
                                      },
                                      {
                                        "Worker Number": 1,
                                        "Actual Startup Time": 0.009,
                                        "Actual Total Time": 0.009,
                                        "Actual Rows": 0,
                                        "Actual Loops": 55940
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
    QEP(op).resolve()
    assert_test(op)


def test_general_3():
    op = {
        "Node Type": "Limit",
        "Parallel Aware": False,
        "Async Capable": False,
        "Startup Cost": 49930.82,
        "Total Cost": 113901.07,
        "Plan Rows": 1,
        "Plan Width": 24,
        "Actual Startup Time": 820.487,
        "Actual Total Time": 826.935,
        "Actual Rows": 1,
        "Actual Loops": 1,
        "Output": ["orders.o_orderpriority", "(count(*))"],
        "Plans": [
          {
            "Node Type": "Aggregate",
            "Strategy": "Sorted",
            "Partial Mode": "Simple",
            "Parent Relationship": "Outer",
            "Parallel Aware": False,
            "Async Capable": False,
            "Startup Cost": 49930.82,
            "Total Cost": 369782.08,
            "Plan Rows": 5,
            "Plan Width": 24,
            "Actual Startup Time": 820.485,
            "Actual Total Time": 826.933,
            "Actual Rows": 1,
            "Actual Loops": 1,
            "Output": ["orders.o_orderpriority", "count(*)"],
            "Group Key": ["orders.o_orderpriority"],
            "Plans": [
              {
                "Node Type": "Nested Loop",
                "Parent Relationship": "Outer",
                "Parallel Aware": False,
                "Async Capable": False,
                "Join Type": "Semi",
                "Startup Cost": 49930.82,
                "Total Cost": 369371.50,
                "Plan Rows": 82105,
                "Plan Width": 16,
                "Actual Startup Time": 235.266,
                "Actual Total Time": 817.405,
                "Actual Rows": 56715,
                "Actual Loops": 1,
                "Output": ["orders.o_orderpriority"],
                "Inner Unique": False,
                "Plans": [
                  {
                    "Node Type": "Gather Merge",
                    "Parent Relationship": "Outer",
                    "Parallel Aware": False,
                    "Async Capable": False,
                    "Startup Cost": 49930.39,
                    "Total Cost": 85650.54,
                    "Plan Rows": 306699,
                    "Plan Width": 20,
                    "Actual Startup Time": 235.148,
                    "Actual Total Time": 282.878,
                    "Actual Rows": 61863,
                    "Actual Loops": 1,
                    "Output": ["orders.o_orderpriority", "orders.o_orderkey"],
                    "Workers Planned": 2,
                    "Workers Launched": 2,
                    "Plans": [
                      {
                        "Node Type": "Sort",
                        "Parent Relationship": "Outer",
                        "Parallel Aware": False,
                        "Async Capable": False,
                        "Startup Cost": 48930.37,
                        "Total Cost": 49249.84,
                        "Plan Rows": 127791,
                        "Plan Width": 20,
                        "Actual Startup Time": 197.660,
                        "Actual Total Time": 207.949,
                        "Actual Rows": 21372,
                        "Actual Loops": 3,
                        "Output": ["orders.o_orderpriority", "orders.o_orderkey"],
                        "Sort Key": ["orders.o_orderpriority"],
                        "Sort Method": "external merge",
                        "Sort Space Used": 3608,
                        "Sort Space Type": "Disk",
                        "Workers": [
                          {
                            "Worker Number": 0,
                            "Actual Startup Time": 182.093,
                            "Actual Total Time": 188.606,
                            "Actual Rows": 19833,
                            "Actual Loops": 1,
                            "Sort Method": "external merge",
                            "Sort Space Used": 2752,
                            "Sort Space Type": "Disk"
                          },
                          {
                            "Worker Number": 1,
                            "Actual Startup Time": 186.147,
                            "Actual Total Time": 200.515,
                            "Actual Rows": 19833,
                            "Actual Loops": 1,
                            "Sort Method": "external merge",
                            "Sort Space Used": 2752,
                            "Sort Space Type": "Disk"
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
                            "Plan Rows": 127791,
                            "Plan Width": 20,
                            "Actual Startup Time": 0.587,
                            "Actual Total Time": 124.056,
                            "Actual Rows": 103159,
                            "Actual Loops": 3,
                            "Output": ["orders.o_orderpriority", "orders.o_orderkey"],
                            "Filter": "((orders.o_orderdate >= '1995-01-01'::date) AND (orders.o_orderdate < '1996-05-10 00:00:00'::timestamp without time zone))",
                            "Rows Removed by Filter": 396841,
                            "Workers": [
                              {
                                "Worker Number": 0,
                                "Actual Startup Time": 1.063,
                                "Actual Total Time": 115.843,
                                "Actual Rows": 93452,
                                "Actual Loops": 1
                              },
                              {
                                "Worker Number": 1,
                                "Actual Startup Time": 0.634,
                                "Actual Total Time": 117.338,
                                "Actual Rows": 93408,
                                "Actual Loops": 1
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
                    "Total Cost": 2.50,
                    "Plan Rows": 5,
                    "Plan Width": 4,
                    "Actual Startup Time": 0.008,
                    "Actual Total Time": 0.008,
                    "Actual Rows": 1,
                    "Actual Loops": 61863,
                    "Output": ["lineitem.l_orderkey", "lineitem.l_partkey", "lineitem.l_suppkey", "lineitem.l_linenumber", "lineitem.l_quantity", "lineitem.l_extendedprice", "lineitem.l_discount", "lineitem.l_tax", "lineitem.l_returnflag", "lineitem.l_linestatus", "lineitem.l_shipdate", "lineitem.l_commitdate", "lineitem.l_receiptdate", "lineitem.l_shipinstruct", "lineitem.l_shipmode", "lineitem.l_comment"],
                    "Index Cond": "(lineitem.l_orderkey = orders.o_orderkey)",
                    "Rows Removed by Index Recheck": 0,
                    "Filter": "(lineitem.l_commitdate < lineitem.l_receiptdate)",
                    "Rows Removed by Filter": 1
                  }
                ]
              }
            ]
          }
        ]
      }
    QEP(op).resolve()
    assert_test(op)