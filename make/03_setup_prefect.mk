.PHONY: create-prefect-blocks
create-prefect-blocks: ## Create Prefect Blocks
	make env-init
	prefect block register --file src/prefect/blocks/create_gcp_credentials.py