##@ [Infrastructure: Setup]

.PHONY: create-gcs-buckets
create-gcs-buckets: ### Create Google Cloud Storage Buckets
	for event_type in watch-events push-events; do \
		gsutil mb -c standard -l ${GCP_DEFAULT_REGION} gs://github-$$event_type-$(ENV) || true; \
	done

.PHONY: create-github-event-publisher-artifact-repository
create-github-event-publisher-artifact-repository: ## Create GCP Artificat Repository for Github Event Publisher/Producer
	make env-init
	gcloud artifacts repositories create $(GITHUB_EVENT_PUBLISHER_NAME)-$(ENV) --repository-format DOCKER --location $(GCP_DEFAULT_REGION)
	gcloud auth configure-docker \
		$(GCP_DEFAULT_REGION)-docker.pkg.dev

.PHONY: push-github-event-publisher-image
push-github-event-publisher-image: ## Push Github Event Publisher/Producer to Artifact Registry
	make env-init
	docker build -t $(GCP_DEFAULT_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(GITHUB_EVENT_PUBLISHER_NAME)-${ENV}/python$(PYTHON_VERSION) \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg POETRY_VERSION=${POETRY_VERSION} \
		--build-arg POETRY_HOME=${POETRY_HOME} \
		--build-arg POETRY_VENV=${POETRY_VENV} \
		--build-arg POETRY_CACHE_DIR=${POETRY_CACHE_DIR} \
		-f images/$(GITHUB_EVENT_PUBLISHER_NAME)/Dockerfile .
	docker push $(GCP_DEFAULT_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(GITHUB_EVENT_PUBLISHER_NAME)-${ENV}/python$(PYTHON_VERSION)

.PHONY: create-github-event-publisher-vm
create-github-event-publisher-vm: ### Create Google Cloud VM which produces/publishes Github Events
	gcloud compute instances create-with-container $(GITHUB_EVENT_PUBLISHER_NAME)-vm-${ENV} \
		--container-image $(GCP_DEFAULT_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/$(GITHUB_EVENT_PUBLISHER_NAME)-${ENV}/python$(PYTHON_VERSION) \
		--container-mount-host-path=host-path=/var/run/docker.sock,mount-path=/var/run/docker.sock,mode=rw \
		--container-privileged \
		--container-stdin \
		--container-tty \
		--container-env-file base.env \
		--container-env ENV=${ENV} \
		--boot-disk-size="200Gi" \
		--machine-type="e2-micro" \
		--zone=$(GCP_DEFAULT_ZONE)

.PHONY: delete-github-event-publisher-vm
delete-github-event-publisher-vm: ### Delete Google Cloud VM which produces/publishes Github Events
	gcloud compute instances delete $(GITHUB_EVENT_PUBLISHER_NAME)-vm-${ENV}

# see https://cloud.google.com/compute/docs/instances/startup-scripts

# 		--container-restart-policy='always' \
# --container-command="prefect" \
# --container-arg="worker" \

# --container-arg="--pool" \
# --container-arg="${ENV}-vertex-ai-work-pool" \
