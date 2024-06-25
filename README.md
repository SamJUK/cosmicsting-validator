A [Cosmicsting POC](https://github.com/Chocapikk/CVE-2024-34102), with a bash script to check all of our hosted sites to confirm the patch.

This repository is provided to allow store owners / hosts to confirm the patch is applied on stores. Within `check.bash` add domains to the `SITES` list.

## Usage
```sh
# Create a python vitual environment for the project
python -m venv venv

# Install the requirements
pip install -r requirements.txt

# Run the check script (to execute against all of our domains)
./check.bash

# Run the POC against a single URL
./poc.py -u https://samdjames.uk
```

