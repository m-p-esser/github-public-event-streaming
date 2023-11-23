""" Pull Github Events using an existing Subscription """

from google.api_core import retry
from google.cloud import pubsub_v1
from icecream import ic

from src.utils import load_env_vars


def pull_events():
    """Pull Events from Watch Topic using Google Pub/Sub using Subscription"""
    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, f"github-event-{environment}"
    )

    with subscriber:
        response = subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 10,
            },
            retry=retry.Retry(deadline=120),
        )
        if len(response.received_messages) == 0:
            ic("No messages received")

        if len(response.received_messages) > 0:
            acknowledgment_ids = []
            for received_message in response.received_messages:
                ic(received_message)
                acknowledgment_ids.append(received_message.ack_id)

            subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": acknowledgment_ids,
                }
            )
            print(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )


if __name__ == "__main__":
    pull_events()
