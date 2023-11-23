""" Create Google Cloud Storage Buckets """

import pathlib

import hydra
from google.cloud import storage
from google.cloud.exceptions import Conflict
from google.oauth2 import service_account
from omegaconf import DictConfig

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


def construct_storage_client(account_file_path: pathlib.Path) -> storage.Client:
    """Construct Storage Client"""

    credentials = service_account.Credentials.from_service_account_file(
        account_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    storage_client = storage.Client(
        credentials=credentials, project=credentials.project_id
    )
    return storage_client


def create_bucket(
    storage_client: storage.Client, bucket: str, location: str, config: dict
) -> storage.Bucket:
    """Create GCS Bucket"""

    bucket = storage_client.bucket(bucket)
    bucket.add_lifecycle_delete_rule(
        age=config["lifecycle_delete_rule_age"]
    )  # delete after N days
    bucket.storage_class = config["storage_class"]
    bucket = storage_client.create_bucket(bucket_or_name=bucket, location=location)
    rules = bucket.lifecycle_rules

    print(f"Created Bucket: '{bucket.name}'")
    print(
        f"Lifecycle management is enable for bucket '{bucket.name}' and the rules are: {list(rules)}"
    )

    return bucket


@hydra.main(config_path="../conf", config_name="config")
def create_gcs_buckets(cfg: DictConfig):
    account_file_path = (
        pathlib.Path.cwd().parent.parent.parent
        / ".secrets"
        / "deployment_sa_account.json"
    )
    env_vars = load_env_vars()
    ENV = env_vars["ENV"]
    GCP_DEFAULT_REGION = env_vars["GCP_DEFAULT_REGION"]

    storage_client = construct_storage_client(account_file_path=account_file_path)

    event_types = cfg.params.event_types
    for event_type in event_types:
        event_type_lowercase_hyphen = pascal_case_to_lower_case_with_hyphen(event_type)
        gcs_bucket_config = cfg.gcs_bucket_config
        bucket = f"github-{event_type_lowercase_hyphen}-{ENV}"
        try:
            create_bucket(
                storage_client=storage_client,
                bucket=bucket,
                location=GCP_DEFAULT_REGION,
                config=gcs_bucket_config,
            )
        except Conflict as e:
            print(f"Error occured while trying to create '{bucket}'")
            print(e)


if __name__ == "__main__":
    create_gcs_buckets()
