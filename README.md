## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/ImperialCollegeLondon/finesse_processing) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/ImperialCollegeLondon/finesse_processing)](https://github.com/ImperialCollegeLondon/finesse_processing) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-finesse_processing-00a3e3.svg)](https://www.research-software.nl/software/finesse_processing) [![workflow pypi badge](https://img.shields.io/pypi/v/finesse_processing.svg?colorB=blue)](https://pypi.python.org/project/finesse_processing/) |
| (4/5) citation                     | |
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>/badge)](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **Other best practices**           | &nbsp; |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/ImperialCollegeLondon/finesse_processing/actions/workflows/build.yml/badge.svg)](https://github.com/ImperialCollegeLondon/finesse_processing/actions/workflows/build.yml) |
## How to use finesse_processing

Code for callibrating FINESSE interferograms

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Installation

To install finesse_processing from GitHub repository, do:

```console
git clone git@github.com:ImperialCollegeLondon/finesse_processing.git
cd finesse_processing
python -m pip install .
```

## Documentation
This is for the FINESSE instrument at Imperial. It is processing code that includes callibration and plotting. This is only python code, there is also an IDL version.

## Python code multi
This folder contains various scripts which are going to be sorted in a functions file and then scripts for running. At the moment there are about 5 scripts, we aim to get it into 2 or 3.
The details of how these scripts are going to be sorted are in the projects workflow thingy/issues!

Here is a description of what each of the files currently does:

- **File 0**  is just reading the sensors to track BB temperatures, PRT sensors and vaisala instrument pressure temperutre humidity + co2

- **File 1**  is preparing the interferograms for single or multi (averaged 40)

- **File 2** is calculating the response functions (always done in multi case)

- **File 3a single** is doing calibration for multi case [NOTE THIS CODE IS NOT FINISHED]
- **File 3b mulit**  is doing calibration for single case 

**Quick plot file:**
- For checking the final calibration spectra output 
- Features to add: Time evolution plots


# src folder
This will eventually contain all the functions needed to run the processing code.
We will then reach out about how to better package these in the end of November 2024


## Credits

This package was created with [Copier](https://github.com/copier-org/copier) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
