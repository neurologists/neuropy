# Copyright 2019 The NeuroPy Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging

from src.utility.arguments import get_arguments
from src.utility.printer import Color, colorprint
from src.utility.configuration import load_project_configuration
from src.utility.validator import validate_project
from src.utility.validator import validate_optional_arguments
from src.agent import Agent

def run(arguments):
    output = None

    # Get configuration
    configuration = load_project_configuration(arguments.configuration)

    # Validate project configuration
    validate_project(configuration)

    # Validate optional paths if present
    validate_optional_arguments(arguments)

    # Set Tensorflow verbosity
    print('TensorFlow debugging set to:', end=' ')
    logger = logging.getLogger('tensorflow')
    if arguments.debug:
        logger.setLevel(logging.DEBUG)
        colorprint(Color.GREEN, "DEBUG")
    elif arguments.verbose:
        logger.setLevel(logging.INFO)
        colorprint(Color.GREEN, "VERBOSE")
    else:
        logger.setLevel(logging.CRITICAL)
        colorprint(Color.GREEN, "NONE", end=' ')
        print('(default)')

    # Set up test/train environment
    if not (arguments.infer or arguments.train):
        colorprint(Color.YELLOW, 'Run mode not selected, performing dry run...', end=' ')
        print('(Try `start -h` for more info)')
    
    # Initialize agent
    colorprint(Color.GREEN, 'Initializing agent...')
    agent = Agent(configuration, arguments)
    
    # Start training routine
    if arguments.train:
        colorprint(Color.GREEN, 'Training model...')
        agent.train()

    # Start inference routine
    if arguments.infer:
        colorprint(Color.GREEN, 'Performing inference...')
        output = agent.infer()

    colorprint(Color.GREEN, 'All operations successful. Exiting ' + configuration['name'] + '.')
    print('(Logs saved to ' + os.path.abspath(configuration['logs'])  + ')')
    
    return output