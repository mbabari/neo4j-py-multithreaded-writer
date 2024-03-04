# 
# This script will create some test nodes on Neo4j using multiple threads.
#
# Simulate  Neo4j cluster behavior when a  pod is deleted.
#

import os
import random
import sys
import time

from concurrent.futures import ThreadPoolExecutor
from functools import partial

#pip install loguru

from loguru import logger
from neo4j import GraphDatabase


# Remove the standard stderr logger sink and create a new custom one
logger.remove()
logger.add(
    sys.stdout,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <magenta>{thread.name}</magenta>"
        " | <cyan>{level}</cyan> | {message}"
    ),
)
# Add a file sink with timestamped log file
logger.add(
    "logs/{time:YYYY-MM-DD_HH-mm-ss}.log",
    rotation="1 day",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)


# Vars
executions = 300
workers = 10


neo4j_host = "neo4j://hostname:7687"

neo4j_pass = "yourPassword"

#neo4j_host = os.getenv("NEO4J_BOLT_URL")
#neo4j_pass = os.getenv("NEO4J_PASSWORD")


def create_node(driver, value):
    """Create a test node."""
    with driver.session() as session:
         session.run(  "CREATE (e:TestNode) SET e += {prop: $value};",
                         value=value,)
   # Also tested with 
   # driver.execute_query(
  #     "CREATE (e:TestNode) SET e += {prop: $value};",
   #     value=value,
   # )
         #session.close()

def delete_nodes(driver):
    """Delete test nodes."""
    driver.execute_query(
        "MATCH (e:TestNode) DETACH DELETE e;",
    )


def run_test(driver, iteration):
    """Run the test."""
    init_time = time.time()
    create_node(driver, f"testing-{iteration}")
    time_spent = time.time() - init_time
    logger.info(f"Created testing-{iteration}, Time spent: {time_spent:.2f}")
    # Random sleep between executions
    time.sleep(random.uniform(0.1, 2.0))


def main():
    
    #Uncomment the next two lines for Driver Debug logs
    #from neo4j.debug import watch
    #watch("neo4j", out=sys.stdout)
    
    #Uncomment the next two lines to display the Neo4j driver version
    #from neo4j import __version__ as neo4j_version
    #print(f"Neo4j Python Driver Version: {neo4j_version}")

    neo4j_auth = ("neo4j", neo4j_pass)
    iterations = [i for i in range(executions)]

    with GraphDatabase.driver(neo4j_host, auth=neo4j_auth) as driver:

        work_work = partial(run_test, driver)
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="Worker") as executor:
            executor.map(work_work, iterations)
        # Delete all test nodes when the threads finish
        delete_nodes(driver)
        driver.close()


if __name__ == "__main__":
    main()
