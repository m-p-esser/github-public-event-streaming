""" Subscriber for Github Events """

from google.cloud import pubsub_v1
from icecream import ic

from src.utils import load_env_vars


def create_subscription():
    """Create Subscription for Github events in Google Pub/Sub"""

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, f"github-events-{environment}")
    subscription_path = subscriber.subscription_path(
        project_id, f"github-events-{environment}"
    )

    with subscriber:
        try:
            subscription = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            ic(subscription)
        except Exception as e:
            ic(e)


if __name__ == "__main__":
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    create_subscription()
