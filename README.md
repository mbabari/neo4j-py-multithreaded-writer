This Neo4j Python Driver client will create multiple nodes using a configurable number of worker threads. At the end of the execution the created nodes will be deleted.
This program can be used to test a Neo4j Cluster beaviour. It was used to test connectivity to a Neo4j Kubernetes cluster when a pod is terminated, deleted or scaled down.
<img width="591" alt="image" src="https://github.com/mbabari/neo4j-py-multithreaded-writer/assets/21334212/027e144a-795b-4ec0-b250-a6b52e71ae41">

## Code Description

The `multi-threaded-writer.py` script demonstrates how to write to Neo4j from
multiple threads. The script performs the following steps:

1. Configures the `loguru` logger to emit formatted messages to `stdout` and
   rotate log files in the `logs/` directory.
2. Defines helper functions to create a node and delete all test nodes.
3. Uses `ThreadPoolExecutor` to spawn a configurable number of worker threads
   that call the Neo4j driver concurrently.
4. Each thread creates a node with a unique value, waits briefly, and logs the
   time taken.
5. After all iterations are complete, the script removes the created nodes and
   closes the driver connection.

The default configuration spawns ten worker threads over three hundred
iterations. Update `neo4j_host`, `neo4j_pass`, `executions`, and `workers` to
tailor the test to your environment.
