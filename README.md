[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ImperialCollegeLondon/FINESSE_processing/main.svg)](https://results.pre-commit.ci/latest/github/ImperialCollegeLondon/FINESSE_processing/main)
[![codecov](https://codecov.io/gh/ImperialCollegeLondon/FINESSE_processing/graph/badge.svg?token=DTS433S9E2)](https://codecov.io/gh/ImperialCollegeLondon/FINESSE_processing)
[![CI](https://github.com/ImperialCollegeLondon/FINESSE_processing/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/FINESSE_processing/actions/workflows/ci.yml)

## Badges

(Customize these badges with your own links, and check <https://shields.io/> or <https://badgen.net/> to see which other badges are available.)

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

## Documentation

This is for the FINESSE instrument at Imperial. It is processing code that includes calibration and plotting. This is only python code, there is also an IDL version. Run the code within the Python multi folder.

Here is a description of what each of the script files currently does:

- **File 0**  is just reading the sensors to track BB temperatures, PRT sensors and vaisala instrument pressure temperature humidity + co2

- **File 1**  is preparing the interferograms for single or multi (averaged 40)

- **File 2** is calculating the response functions (always done in multi case)

- **File 3a single** is doing calibration for single case [NOTE THIS CODE IS NOT FINISHED]
- **File 3b multi**  is doing calibration for multi case

**Quick plot file:**

- For checking the final calibration spectra output
- Features to add: Time evolution plots

## How to use finesse_processing

Code for calibrating FINESSE interferograms.

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## For developers

### Download the code

First you need to clone the repository:

```sh
git clone git@github.com:ImperialCollegeLondon/finesse_processing.git
```

### (Optionally) make a virtual environment

We recommend that you create a [virtual environment](https://docs.python.org/3/library/venv.html) for `FINESSE_processing` to keep the packages installed separate. You can do this like so:

```sh
python -m venv .venv
```

You then need to activate it for your shell. If you are using `bash` then you can run:

```sh
source .venv/bin/activate
```

(If you are using a different shell, then there are other scripts in the `.venv/bin` folder you can use instead.)

### Install the developer dependencies

Next you will want to install the dependencies for `FINESSE_processing` along with the developer tools required to work on the project.

You can do this like so:

```sh
pip install -e .[dev,scripts]
```

### Install `pre-commit`

This project contains a configuration file for [`pre-commit`](https://pre-commit.com), a tool which automatically runs specified checks every time you make a commit with Git. The `pre-commit` command-line tool will be installed along with the other developer dependencies, but you **also** have to enable it for this repository, like so:

```sh
pre-commit install
```

Now, whenever you make a Git commit, your changes will be checked for errors and stylistic problems. (For a list of the hooks enabled for this repository, [see the configuration file](./.pre-commit-config.yaml)).

The `pre-commit` hooks will also be run on every pull request by [pre-commit.ci](https://pre-commit.ci).

# `src` folder

This will eventually contain all the functions needed to run the processing code.
We will then reach out about how to better package these in the end of November 2024

# `finesse_simulating` folder

This contains the code to run LBLRTM simulations of FINESSE spectra which is separate from the processing code to read and calibrated FINESSE interferograms.

Code is based on work done by Laura Warwick, Sophie Mosselmans, and Sanjeevani Panditharatne.

Contents include:

- **/src** folder that includes functions and modules used to interact with LBLRTM outputs which should not need to be edited
- **define_inputs.py** which is used to input profile variables, input and output paths, and specify lblrtm version
- **run_lblrtm_FINESSE.py** the script to write the TAPE5, run the exe, and apply the FINESSE instrument line shape
- **/example_input** contains an example profile to be read
- **/example_output** contains an example output and plot
- **EM27_ILS_test1_3_25.sav** is the EM27 ILS used for version 001 of the 2025_WHAFFFERS deliverarables (May 2025)
Required modules are in src/module_function_list.py

## Credits

This package was created with [Copier](https://github.com/copier-org/copier) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
