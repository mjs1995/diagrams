from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import GKE
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.analytics import Trino
from diagrams.onprem.database import MySQL
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.analytics import minio
from diagrams.generic.storage import Storage

with Diagram("GKE Cluster Architecture", show=False, outformat="png"):
    storage = Storage("Data Source")

    with Cluster("Monitoring"):
        metrics = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        metrics - Edge(color="firebrick", style="dashed") - grafana

    with Cluster("GKE Cluster"):
        gke_cluster = GKE("gke-airflow")

        with Cluster("Workflow"):
            airflow = Airflow("Airflow")

        with Cluster("Data Processing"):
            trino_coordinator = Trino("Trino Coordinator")
            with Cluster("Trino Workers"):
                trino_workers = [Trino("Worker1"), Trino("Worker2"), Trino("WorkerX")]
            trino_coordinator - Edge(color="darkgreen", style="bold") - trino_workers

        with Cluster("Object Storage"):
            minio = minio("MinIO")

        with Cluster("Metadata Storage"):
            metastore = MySQL("Hive MetaStore")

    storage >> Edge(label="Source data") >> gke_cluster
    gke_cluster >> Edge(label="Orchestration") >> airflow
    airflow >> Edge(label="Data ingestion") >> minio
    minio >> Edge(label="Query data") >> trino_coordinator
    trino_coordinator >> Edge(label="Metadata") >> metastore
    gke_cluster << Edge(color="darkorange", style="bold") << metrics
