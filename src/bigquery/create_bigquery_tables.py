""" Create Bigquery Tables """

import pathlib

import hydra
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from omegaconf import DictConfig

from src.utils import load_env_vars, pascal_case_to_lower_case_with_hyphen


def construct_bigquery_client(account_file_path, location) -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_file(
        account_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    bigquery_client = bigquery.Client(
        credentials=credentials, project=credentials.project_id, location=location
    )
    return bigquery_client


def create_dataset(bigquery_client: bigquery.Client, location: str, env: str = "dev"):
    """Create Bigquery Dataset"""

    dataset_reference = bigquery.DatasetReference(
        project=bigquery_client.project, dataset_id=env
    )
    dataset_reference.location = location

    try:
        bigquery_client.get_dataset(dataset_reference)
        print(f"Dataset '{dataset_reference}' already exists")
        dataset_exists = True
    except NotFound:
        print(f"Dataset '{dataset_reference}' is not found")
        dataset_exists = False

    if not dataset_exists:
        bigquery_client.create_dataset(dataset_reference)
        print(f"Created dataset '{dataset_reference}'")


def create_bigquery_table_from_gcs_bucket(
    bigquery_client: bigquery.Client,
    table_name: str,
    bucket: str,
    autodetect: bool,
    file_format: str = "AVRO",
    env: str = "dev",
):
    """Create Bigquery Table"""
    dataset_reference = bigquery.DatasetReference(
        project=bigquery_client.project,
        dataset_id=env,
    )

    table_reference = bigquery.TableReference(
        dataset_ref=dataset_reference, table_id=table_name
    )

    table = bigquery.Table(table_ref=table_reference)

    external_config = bigquery.ExternalConfig(file_format)
    source_uri = f"gs://{bucket}/*.{file_format.lower()}"
    external_config.source_uris = [source_uri]
    external_config.autodetect = autodetect
    table.external_data_configuration = external_config

    # Create a permanent table linked to the GCS bucket
    table = bigquery_client.create_table(table)

    print(f"Created Table: '{table.table_id}'")


@hydra.main(config_path="../conf", config_name="config")
def create_bigquery_tables(cfg: DictConfig):
    account_file_path = (
        pathlib.Path.cwd().parent.parent.parent
        / ".secrets"
        / "deployment_sa_account.json"
    )
    env_vars = load_env_vars()
    ENV = env_vars["ENV"]
    GCP_DEFAULT_REGION = env_vars["GCP_DEFAULT_REGION"]

    bigquery_client = construct_bigquery_client(
        account_file_path=account_file_path, location=GCP_DEFAULT_REGION
    )
    with bigquery_client as bqc:
        create_dataset(bigquery_client=bqc, location=GCP_DEFAULT_REGION, env=ENV)

        event_types = cfg.params.event_types

        for event_type in event_types:
            event_type_lowercase_hyphen = pascal_case_to_lower_case_with_hyphen(
                event_type
            )
            bucket = f"github-{event_type_lowercase_hyphen}-{ENV}"

            create_bigquery_table_from_gcs_bucket(
                bigquery_client=bqc,
                table_name=event_type_lowercase_hyphen,
                bucket=bucket,
                autodetect=True,
                file_format="AVRO",
                env=ENV,
            )


if __name__ == "__main__":
    create_bigquery_tables()
