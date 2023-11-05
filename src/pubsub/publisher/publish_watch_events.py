""" Publisher for Github Watch Events """

from ghapi.all import GhApi
from google.cloud import pubsub_v1
from icecream import ic

from src.utils import load_env_vars


def publish_events():
    """Publish Events to Google Pub/Sub Topic"""
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    github_token = env_vars["GITHUB_TOKEN"]

    publisher = pubsub_v1.PublisherClient()
    ghapi = GhApi(token=github_token)

    topic_path = publisher.topic_path(project_id, f"watch-{environment}")

    events = ghapi.list_events()
    for i in events[0:10]:
        message = str(i).encode("utf-8")
        ic(message)

        publish_future = publisher.publish(topic=topic_path, data=message)
        ic(publish_future.result())


if __name__ == "__main__":
    publish_events()
