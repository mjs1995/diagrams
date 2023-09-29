from diagrams import Cluster, Diagram, Edge
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage
from diagrams.programming.language import Python

graph_attrs = {
    "pad": "0.5",
    "rankdir": "TB",  
}

with Diagram("", show=False, graph_attr=graph_attrs):

    with Cluster("user (client)"):
        with Cluster("DML"):
            insert = SQL("INSERT")
            update = SQL("UPDATE")
            delete = SQL("DELETE")
        ddl = SQL("DDL")

    with Cluster("server"):
        with Cluster("MySQL/MariaDB (server/master)"):
            with Cluster("Rows_event"):
                write_rows_event = SQL("Write_rows_event")
                update_rows_event = SQL("Update_rows_event")
                delete_rows_event = SQL("Delete_rows_event")
            query_event = SQL("Query_event")
            binary_log = Storage("binary log")

    with Cluster("MySQL/MariaDB (slave)"):
        execute = SQL("Execute")

    with Cluster("python-mysql-replication (slave)"):
        with Cluster("RowsEvent"):
            writeRowsEvent = SQL("WriteRowsEvent")
            updateRowsEvent = SQL("UpdateRowsEvent")
            deleteRowsEvent = SQL("DeleteRowsEvent")
        queryEvent = SQL("QueryEvent")

    insert >> Edge(label="Write_rows_event") >> write_rows_event
    update >> Edge(label="Update_rows_event") >> update_rows_event
    delete >> Edge(label="Delete_rows_event") >> delete_rows_event
    ddl >> Edge(label="Query_event") >> query_event

    write_rows_event  >> binary_log
    update_rows_event >> binary_log
    delete_rows_event >> binary_log
    query_event >> binary_log

    binary_log >> Edge(label="Execute") >> execute

    binary_log >> Edge(label="WriteRowsEvent") >> writeRowsEvent
    binary_log >> Edge(label="UpdateRowsEvent") >> updateRowsEvent
    binary_log >> Edge(label="DeleteRowsEvent") >> deleteRowsEvent
    binary_log >> Edge(label="QueryEvent") >> queryEvent