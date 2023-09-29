from diagrams import Cluster, Diagram, Edge
from diagrams.aws.database import Dynamodb, Redshift
from diagrams.aws.analytics import KinesisDataStreams, ElasticsearchService
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.onprem.database import MySQL, MariaDB
from diagrams.generic.database import SQL
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark, pymy
from diagrams.saas.analytics import Snowflake

with Diagram("", show=False):

    with Cluster("User (Client)"):
        muser = MySQL("MySQL User")
        mduser = MariaDB("MariaDB User")

    with Cluster("Server"):

        with Cluster("MySQL/MariaDB Master"):
            master = SQL("Binlog")

    with Cluster("MySQL/MariaDB Slave"):
        slave = SQL("Slave")

    with Cluster("python-mysql-replication Slave"):
        py_mysql_replication = pymy("")

    muser >> Edge(label="DDL/DML") >> master
    master >> Edge(label="Event") >> py_mysql_replication
    master >> Edge(label="Execute") >> slave

    with Cluster("UseCase"):
        with Cluster("AWS"):
            kinesis = KinesisDataStreams("Kinesis")
            py_mysql_replication >> kinesis >> Lambda("Lambda") >> [Dynamodb("DynamoDB"), ElasticsearchService("OpenSearch Service")]
            py_mysql_replication >> S3("S3") >> Redshift("Redshift")

        py_mysql_replication >> Kafka("Kafka") >> Spark("Spark\n Streaming") >> Snowflake("Snowflake")