qepObject = {
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