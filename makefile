runserver:
	docker compose -f docker-compose-dev.yml down
	docker compose -f docker-compose-dev.yml up

test:
	docker compose -f docker-compose-test.yml down
	docker compose -f docker-compose-test.yml run --rm twitter_api_test || true
	docker compose -f docker-compose-test.yml down

