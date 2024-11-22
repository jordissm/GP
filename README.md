# Hadron formation time cross-sections using Gaussian Processes
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Tool for creating various functional forms for time-dependent cross-sections useful to understand hadron formation in a model independent fashion. For physics details, please refer to [arXiv:2501:XXXXX](www.arxiv.org/abs/2501.XXXXX).

## Dependencies
The following Python libraries are required for sucessful results:
- pyyaml
- numpy
- pandas
- matplotlib
- openapi-core

which can be installed through
```bash
pip install pyyaml numpy pandas matplotlib openapi-core
```

## Usage
Generation of time-dependent cross-section functional forms is performed by executing
```bash
python3 src/main.py input/config.yml
```

The output will be witten to the `output` directory in tabular form, along with the corresponding plots of generated data.

## Notes
- Ensure all dependencies are installed.
- Adjust hyperparameters in `config.yaml` to experiment with different cross-section behaviors.

## Acknowledgements
This work has been supported by the Sateurated Glue (SURGE) Topical Theory Collaboration.