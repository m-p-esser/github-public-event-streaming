""" Publisher for Github Watch Events """

import hydra
from ghapi.all import GhApi
from google.cloud import pubsub_v1
from icecream import ic

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


@hydra.main(config_path="../../conf", config_name="config")
def publish_events(cfg):
    """Publish Events to Google Pub/Sub Topic"""

    event_type = cfg["params"]["active_event_type"]
    event_type_lowercase_hyphen = pascal_case_to_lower_case_with_hyphen(event_type)

    publisher = pubsub_v1.PublisherClient()
    ghapi = GhApi(token=github_token)

    topic_path = publisher.topic_path(project_id, f"github-events-{environment}")

    events = ghapi.fetch_events(types=event_type)
    for i in events:
        message = str(i).encode("utf-8")
        ic(message)

        publish_future = publisher.publish(
            topic=topic_path, data=message, event_type=event_type_lowercase_hyphen
        )
        ic(publish_future.result())


if __name__ == "__main__":
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    github_token = env_vars["GITHUB_TOKEN"]
    publish_events()
