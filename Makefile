.PHONY: run
run:
	@alembic upgrade head
	@uvicorn app:app --reload --host 0.0.0.0 --port ${PORT} --log-level "info" --ws-ping-interval 300
