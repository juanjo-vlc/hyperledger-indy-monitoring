import logging
import json
from datetime import datetime

LOGGER = logging.getLogger(__name__)

ledger_names = ['ledger', 'pool', 'config', 'audit']
date_fmt = '%Y-%m-%d %H:%M:%S+00:00'

def generate_metrics(validator_info):
    #LOGGER.debug(json.dumps(validator_info, indent=2))
    metrics = []

    metrics.append("#TYPE indynode_uptime gauge")
    metrics.append("#TYPE indynode_replicas gauge")
    metrics.append("#TYPE indynode_synced gauge")
    metrics.append("#TYPE indynode_uncommited_txns gauge")

    for obj in validator_info:
        if "Node_info" in obj:
            node = obj["Node_info"]["Name"].lower()
            metrics.append("indynode_timestamp{node=\"" + node + "\"} " + str(obj["timestamp"]))
            metrics.append("indynode_delta{node=\"" + node + "\"} " + str(obj["Node_info"]["Metrics"]["Delta"]))
            metrics.append("indynode_lambda{node=\"" + node + "\"} " + str(obj["Node_info"]["Metrics"]["Lambda"]))
            metrics.append("indynode_omega{node=\"" + node + "\"} " + str(obj["Node_info"]["Metrics"]["Omega"]))
            metrics.append("indynode_uptime{node=\"" + node + "\"} " + str(obj["Node_info"]["Metrics"]["uptime"]))
            metrics.append("indynode_replicas{node=\"" + node + "\"} " + str(obj["Node_info"]["Count_of_replicas"]))
            metrics.append("indynode_master_instance_started{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["instances started"]["0"]))
            #metrics.append("indynode_client_instance_started{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["instances started"]["1"]))
            metrics.append("indynode_master_ordered_request_counts{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["ordered request counts"]["0"]))
            #metrics.append("indynode_client_ordered_request_counts{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["ordered request counts"]["1"]))
            metrics.append("indynode_master_throughput{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["throughput"]["0"]))
            #metrics.append("indynode_client_throughput{node=\"" + node + "\"} "+ str(obj["Node_info"]["Metrics"]["throughput"]["1"]))
            for k,v in obj["Node_info"]["Metrics"]["transaction-count"].items():
                metrics.append("indynode_transactions{node=\"" + node + "\",ledger=\"" +  k +"\"} "+ str(v))
            metrics.append("indynode_synced{node=\"" + node + "\",ledger=\"ledger\"} " + str(int(obj["Node_info"]["Catchup_status"]["Ledger_statuses"]["0"] == "synced")))
            metrics.append("indynode_synced{node=\"" + node + "\",ledger=\"pool\"} " + str(int(obj["Node_info"]["Catchup_status"]["Ledger_statuses"]["1"] == "synced")))
            metrics.append("indynode_synced{node=\"" + node + "\",ledger=\"config\"} " + str(int(obj["Node_info"]["Catchup_status"]["Ledger_statuses"]["2"] == "synced")))
            metrics.append("indynode_synced{node=\"" + node + "\",ledger=\"audit\"} " + str(int(obj["Node_info"]["Catchup_status"]["Ledger_statuses"]["3"] == "synced")))

            metrics.append("indynode_uncommited_txns{node=\"" + node + "\",ledger=\"ledger\"} " + str(obj["Node_info"]["Uncommitted_ledger_txns"]["0"]["Count"]))
            metrics.append("indynode_uncommited_txns{node=\"" + node + "\",ledger=\"pool\"} " + str(obj["Node_info"]["Uncommitted_ledger_txns"]["1"]["Count"]))
            metrics.append("indynode_uncommited_txns{node=\"" + node + "\",ledger=\"config\"} " + str(obj["Node_info"]["Uncommitted_ledger_txns"]["2"]["Count"]))
            metrics.append("indynode_uncommited_txns{node=\"" + node + "\",ledger=\"audit\"} " + str(obj["Node_info"]["Uncommitted_ledger_txns"]["3"]["Count"]))

            metrics.append("indynode_txn_in_catchup{node=\"" + node + "\",ledger=\"ledger\"} " + str(obj["Node_info"]["Catchup_status"]["Number_txns_in_catchup"]["0"]))
            metrics.append("indynode_txn_in_catchup{node=\"" + node + "\",ledger=\"pool\"} " + str(obj["Node_info"]["Catchup_status"]["Number_txns_in_catchup"]["1"]))
            metrics.append("indynode_txn_in_catchup{node=\"" + node + "\",ledger=\"config\"} " + str(obj["Node_info"]["Catchup_status"]["Number_txns_in_catchup"]["2"]))
            metrics.append("indynode_txn_in_catchup{node=\"" + node + "\",ledger=\"audit\"} " + str(obj["Node_info"]["Catchup_status"]["Number_txns_in_catchup"]["3"]))

            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"ledger\"} " + str(datetime.strptime(obj["Node_info"]["Freshness_status"]["0"]["Last_updated_time"], date_fmt).timestamp()))
            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"pool\"} " + str(datetime.strptime(obj["Node_info"]["Freshness_status"]["1"]["Last_updated_time"], date_fmt).timestamp()))
            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"config\"} " + str(datetime.strptime(obj["Node_info"]["Freshness_status"]["2"]["Last_updated_time"], date_fmt).timestamp()))
            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"ledger\"} " + str(int(obj["Node_info"]["Freshness_status"]["0"]["Has_write_consensus"])))
            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"pool\"} " + str(int(obj["Node_info"]["Freshness_status"]["1"]["Has_write_consensus"])))
            metrics.append("indynode_last_updated{node=\"" + node + "\",ledger=\"config\"} " + str(int(obj["Node_info"]["Freshness_status"]["2"]["Has_write_consensus"])))

    return "\n".join(metrics)+"\n"
