""" GCS Subscriber for Github Events """

import hydra
from google.cloud import pubsub_v1
from omegaconf import DictConfig

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


@hydra.main(config_path="../../conf", config_name="config")
def create_gcs_subscriptions(cfg: DictConfig):
    """Create Google Cloud Storage Subscriptions for Events in Google Pub/Sub"""

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, f"github-event-{environment}")

    event_types = cfg.params.event_types

    with subscriber:
        for event_type in event_types:
            event_type_lower_case_hyphen = pascal_case_to_lower_case_with_hyphen(
                event_type
            )
            filename_prefix = event_type
            filename_suffix = ".avro"
            avro_config = pubsub_v1.types.CloudStorageConfig.AvroConfig(
                write_metadata=True
            )
            bucket = f"github-{event_type_lower_case_hyphen}-{environment}"

            try:
                # GCS Bucket Subscriber
                subscription_path = subscriber.subscription_path(
                    project_id, f"{event_type_lower_case_hyphen}-gcs-{environment}"
                )

                cloud_storage_config = pubsub_v1.types.CloudStorageConfig(
                    bucket=bucket,
                    filename_prefix=filename_prefix,
                    filename_suffix=filename_suffix,
                    avro_config=avro_config,
                )

                filter = f'attributes.event_type = "{event_type_lower_case_hyphen}"'
                subscription = subscriber.create_subscription(
                    request={
                        "name": subscription_path,
                        "topic": topic_path,
                        "cloud_storage_config": cloud_storage_config,
                        "filter": filter,
                    }
                )
                print(f"Cloud Storage subscription created: {subscription}.")
                print(f"Bucket for subscription is: {bucket}")
                print(f"Prefix is: {filename_prefix}")
                print(f"Suffix is: {filename_suffix}")
                print(f"Active Filter: {filter}")
            except Exception as e:
                print(
                    f"An error occured when trying to create Cloud Storage subscription for: {event_type}"
                )
                print(e)


if __name__ == "__main__":
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]
    create_gcs_subscriptions()
