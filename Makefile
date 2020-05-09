docker:
	docker build -t heiseish/dawnpy:1.0.0 -f Dockerfile .
py-format:
	yapf -r -p -i src