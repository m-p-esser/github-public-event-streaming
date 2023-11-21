##@ [Infrastructure: Setup]

.PHONY: create-gcs-buckets
create-gcs-buckets: ### Create Google Cloud Storage Buckets
	for event_type in watch-events push-events; do \
		gsutil mb -c standard -l ${GCP_DEFAULT_REGION} gs://github-$$event_type-$(ENV) || true; \
	done 


	