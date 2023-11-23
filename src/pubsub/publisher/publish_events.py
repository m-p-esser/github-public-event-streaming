""" Publisher for Github Watch Events """

from ghapi.all import GhApi
from google.cloud import pubsub_v1
from icecream import ic
from prefect.task_runners import ConcurrentTaskRunner

from prefect import flow, task
from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


@flow(task_runner=ConcurrentTaskRunner())
def fetch_events():
    """Fetch Events from Github Events API"""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, f"github-event-{environment}")

    ghapi = GhApi(token=github_token)
    events = ghapi.fetch_events(n_pages=3, pause=3, per_page=10)

    for e in events:
        event_type = e["type"]
        event_type_lowercase_hyphen = pascal_case_to_lower_case_with_hyphen(event_type)
        send_message.submit(e, publisher, topic_path, event_type_lowercase_hyphen)


@task
def send_message(event, publisher, topic_path, event_type):
    """Publish Events as messages to Google Pub/Sub Topic"""

    message = str(event).encode("utf-8")
    ic(message)

    # publish_future = publisher.publish(topic=topic_path, data=message, event_type=event_type)
    # ic(publish_future.result())


@flow
# @hydra.main(config_path="../../conf", config_name="config")
def publish_events():
    """Publish Events to Google Pub/Sub Topic"""
    fetch_events()


if __name__ == "__main__":
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    github_token = env_vars["GITHUB_TOKEN"]
    publish_events()
