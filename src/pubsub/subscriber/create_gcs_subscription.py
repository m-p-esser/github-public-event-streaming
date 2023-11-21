""" GCS Subscriber for Github Events """

import hydra
from google.cloud import pubsub_v1

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


@hydra.main(config_path="../../conf", config_name="config")
def create_gcs_subscriptions(cfg):
    """Create Google Cloud Storage Subscriptions for Events in Google Pub/Sub"""

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, f"github-events-{environment}")

    event_types = [cfg["params"]["event_types"][-1]]
    for event_type in event_types:
        event_type_lower_case_hyphen = pascal_case_to_lower_case_with_hyphen(event_type)

        # GCS Bucket Subscriber
        subscription_path = subscriber.subscription_path(
            project_id, f"{event_type_lower_case_hyphen}-gcs-{environment}"
        )

        cloud_storage_config = pubsub_v1.types.CloudStorageConfig(
            bucket=f"github-watch-events-{environment}",
        )

        with subscriber:
            filter = f'attributes.event_type = "{event_type_lower_case_hyphen}"'
            subscription = subscriber.create_subscription(
                request={
                    "name": subscription_path,
                    "topic": topic_path,
                    "cloud_storage_config": cloud_storage_config,
                    "filter": filter,
                }
            )
            print(
                f"Created Google Cloud Storage subscription for Event: {event_type}: {subscription}. The following filter rule is active: {filter}"
            )


if __name__ == "__main__":
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    create_gcs_subscriptions()
