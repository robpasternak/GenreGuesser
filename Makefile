# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* GenreGuesser/*.py

black:
	@black scripts/* GenreGuesser/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr GenreGuesser-*.dist-info
	@rm -fr GenreGuesser.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)




APP_NAME = superduper-genre-guesser
streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

##### Prediction API - - - - - - - - - - - - - - - - - - - - - - - - -

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload


# ----------------------------------
#      UPLOAD PACKAGE TO GCP
# ----------------------------------

# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH=raw_data/rap_data.csv

# project id
PROJECT_ID=affable-elf-337812

# bucket name
BUCKET_NAME=lewagon-815-genre-guesser

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

REGION=europe-west1

set_project:
	-@gcloud config set project ${PROJECT_ID}

create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
# -@gsutil cp train_1k.csv gs://wagon-ml-my-bucket-name/data/train_1k.csv
	-@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

##### Package params  - - - - - - - - - - - - - - - - - - -

PACKAGE_NAME=GenreGuesser
FILENAME=training


run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs

fit_knn:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit knn

fit_gb:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit gb

fit_svm:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit svm

fit_rfc:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit rfc

fit_knn_final:
	@python -m ${PACKAGE_NAME}.${FILENAME} finalfit knn

fit_gb_final:
	@python -m ${PACKAGE_NAME}.${FILENAME} finalfit gb

fit_svm_final:
	@python -m ${PACKAGE_NAME}.${FILENAME} finalfit svm

fit_rfc_final:
	@python -m ${PACKAGE_NAME}.${FILENAME} finalfit rfc

fit_nbc:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit nbc

fit_all:
	@python -m ${PACKAGE_NAME}.${FILENAME} localfit knn svm gb rfc

cv_knn:
	@python -m ${PACKAGE_NAME}.${FILENAME} cross_val knn

cv_gb:
	@python -m ${PACKAGE_NAME}.${FILENAME} cross_val gb

cv_svm:
	@python -m ${PACKAGE_NAME}.${FILENAME} cross_val svm

cv_rfc:
	@python -m ${PACKAGE_NAME}.${FILENAME} cross_val rfc

cv_nbc:
	@python -m ${PACKAGE_NAME}.${FILENAME} cross_val nbc

one_split_knn:
	@python -m ${PACKAGE_NAME}.${FILENAME} one_split knn

one_split_gb:
	@python -m ${PACKAGE_NAME}.${FILENAME} one_split gb

one_split_svm:
	@python -m ${PACKAGE_NAME}.${FILENAME} one_split svm

one_split_rfc:
	@python -m ${PACKAGE_NAME}.${FILENAME} one_split rfc

one_split_nbc:
	@python -m ${PACKAGE_NAME}.${FILENAME} one_split nbc

grid_knn:
	@python -m ${PACKAGE_NAME}.${FILENAME} grid_search knn

grid_gb:
	@python -m ${PACKAGE_NAME}.${FILENAME} grid_search gb

grid_svm:
	@python -m ${PACKAGE_NAME}.${FILENAME} grid_search svm

grid_rfc:
	@python -m ${PACKAGE_NAME}.${FILENAME} grid_search rfc

grid_nbc:
	@python -m ${PACKAGE_NAME}.${FILENAME} grid_search nbc
