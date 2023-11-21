from google.cloud import pubsub_v1

from src.utils import load_env_vars


def create_topics():
    """Create Google Pub/Sub topics"""

    env_vars = load_env_vars()
    project_id = env_vars["GCP_PROJECT_ID"]
    environment = env_vars["ENV"]

    publisher = pubsub_v1.PublisherClient()

    topics_paths = [publisher.topic_path(project_id, f"github-events-{environment}")]
    for topic_path in topics_paths:
        try:
            topic = publisher.create_topic(request={"name": topic_path})
            print(f"Sucessfully created topic '{topic.name}'")
        except Exception as e:
            print(f"Failed to create topic '{topic.name}': {e}")


if __name__ == "__main__":
    create_topics()
