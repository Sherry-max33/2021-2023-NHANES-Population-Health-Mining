# Simple command shortcuts
.PHONY: data features train eval clean

data:
	python -m src.data --check

features:
	python -m src.features --build

train:
	python -m src.models --train --config configs/default.yml

eval:
	python -m src.models --eval

clean:
	rm -rf __pycache__ */__pycache__ .ipynb_checkpoints
