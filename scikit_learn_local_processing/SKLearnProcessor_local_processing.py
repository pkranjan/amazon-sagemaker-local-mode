# This is a sample Python program that runs a simple scikit-learn processing using the SKLearnProcessor.
# This implementation will work on your *local computer*.
#
# Prerequisites:
#   1. Install required Python packages:
#       pip install boto3 sagemaker pandas scikit-learn
#       pip install 'sagemaker[local]'
#   2. Docker Desktop installed and running on your computer:
#      `docker ps`
#   3. You should have AWS credentials configured on your local machine
#      in order to be able to pull the docker image from ECR.
########################################################################################################################

import os
from sagemaker.local import LocalSession
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor

sagemaker_session = LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# For local training a dummy role will be sufficient
role = 'arn:aws:iam::111111111111:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001'

processor = SKLearnProcessor(framework_version='0.20.0',
                             instance_count=1,
                             instance_type='local',
                             role=role)

print('Starting processing job.')
print('Note: if launching for the first time in local mode, container image download might take a few minutes to complete.')
processor.run(code='processing_script.py',
                      inputs=[ProcessingInput(
                          source='./input_data/',
                          destination='/opt/ml/processing/input_data/')],
                      outputs=[ProcessingOutput(
                          output_name='word_count_data',
                          source='/opt/ml/processing/processed_data/')],
                      arguments=['job-type', 'word-count']
                     )

preprocessing_job_description = processor.jobs[-1].describe()
output_config = preprocessing_job_description['ProcessingOutputConfig']

print(output_config)

for output in output_config['Outputs']:
    if output['OutputName'] == 'word_count_data':
        word_count_data_file = output['S3Output']['S3Uri']

print('Output file is located on: {}'.format(word_count_data_file))