.ONESHELL:
.EXPORT_ALL_VARIABLES:
.DEFAULT_GOAL := help

SHELL = /bin/bash
PATH := venv/bin:$(PATH)


help:
	echo "Volcanic project under construction..."
.PHONY: help

venv:
	python3 -m venv venv
	pip3 install --upgrade pip
	pip3 install numpy Pillow PyOpenGL PyOpenGL-accelerate glfw cython AssimpCy

run: venv
	python3 sources/viewer.py assets/suzanne.obj
.PHONY: run

clean:
	rm -rf venv 2> /dev/null
.PHONY: clean
