.PHONY: help

help:
	@echo "--------------------------------------------------------------------"
	@echo "                    3D Human Post Estimation                        "
	@echo "             BOUN SWE 583 - Computer Vision project                 "
	@echo "--------------------------------------------------------------------"
	@echo "              This Makefile assumes you have Docker                 "
	@echo "--------------------------------------------------------------------"
	@echo "  targets: local, local-mediapipe, docker, docker-mediapipe, help   "
	@echo "--------------------------------------------------------------------"
	@echo "   Local:                                                           "
	@echo "         > make local;                    # input_file: demo.mp4    "
	@echo "         > make local INPUT_FILE=yogi;    # input_file: yogi.mp4    "
	@echo "         > make local INPUT_FILE=dancer;  # input_file: dancer.mp4  "
	@echo "   Local-mediapipe:                                                 "
	@echo "         > make Local-mediapipe;                                    "
	@echo "         > make Local-mediapipe INPUT_FILE=yogi;                    "
	@echo "         > make Local-mediapipe INPUT_FILE=dancer;                  "
	@echo "   Docker:                                                          "
	@echo "         > make docker;                   # input_file: demo.mp4    "
	@echo "         > make docker INPUT_FILE=yogi;   # input_file: yogi.mp4    "
	@echo "         > make docker INPUT_FILE=dancer; # input_file: dancer.mp4  "
	@echo "   Docker (mediapipe):                                              "
	@echo "         > make docker-mediapipe;                                   "
	@echo "         > make docker-mediapipe INPUT_FILE=yogi;                   "
	@echo "         > make docker-mediapipe INPUT_FILE=dancer;                 "
	@echo "   Help:                                                            "
	@echo "         > make;                                                    "
	@echo "         > make help;                                               "
	@echo "--------------------------------------------------------------------"

requirements:
	@python -m pip install -q --upgrade pip
	pip install -qr requirements.txt

INPUT_FILE=demo

local: requirements
	python main.py $(INPUT_FILE)

local-mediapipe: requirements
	python main_mediapipe.py $(INPUT_FILE)

docker-image:
	docker build -t computer-vision .
docker: docker-image
	docker run --rm -it -v ${CURDIR}:/cv computer-vision make local INPUT_FILE=$(INPUT_FILE)

docker-image-mediapipe:
	docker build -t computer-vision-mediapipe .
docker-mediapipe: docker-image-mediapipe
	docker run --rm -it -v ${CURDIR}:/cv computer-vision-mediapipe make local-mediapipe INPUT_FILE=$(INPUT_FILE)
