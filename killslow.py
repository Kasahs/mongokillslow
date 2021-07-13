#!/usr/bin/env python3
"""
Expected in environment:
KS_CONN_URI: mongodb connection string
KS_NAMESPACES: comma separated list of namespaces (usually its <dbname>.<collectionName>)
KS_OPS: comma separated list (from currentOp.type)
KS_MILLISEC_RUNNING: number of milliseconds since the operation began
"""

import os
import pymongo
import logging
import json
from bson.json_util import dumps as bson_to_json

logging.basicConfig(
    format="%(asctime)s  %(levelname)s: %(message)s", level=logging.DEBUG
)


def main():
    logging.info("Connecting...")
    client = pymongo.MongoClient(
        os.getenv("KS_CONN_URI"), serverSelectionTimeoutMS=10000
    )

    try:
        client.server_info()
        logging.info("Connection Successful.")
    except Exception as e:
        logging.error("Connection Failed.")
        logging.error(e)

    admin_db = client.get_database("admin")

    allowed_namespaces = [
        item.strip() for item in str(os.getenv("KS_NAMESPACES")).split(",")
    ]
    allowed_ops = [item.strip() for item in str(os.getenv("KS_OPS")).split(",")]

    query = [
        {"$currentOp": {"allUsers": True, "idleSessions": True}},
        {
            "$match": {
                "active": True,
                "microsecs_running": {
                    "$gte": int(os.getenv("KS_MILLISEC_RUNNING", 10000)) * 1000
                },
                "ns": {"$in": allowed_namespaces},
                "op": {"$in": allowed_ops},
            }
        },
    ]

    logging.info("currentOp query: \n%s\n" % json.dumps(query))

    ops = admin_db.aggregate(query)
    count = 0
    for op in ops:
        res = admin_db.command({"killOp": 1, "op": op["opid"]})
        logging.info("killed: %s" % bson_to_json({"op": op, "kill": res}))

        count += 1

    logging.info("ops found: %d" % count)


if __name__ == "__main__":
    main()
