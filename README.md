A [Cosmicsting POC](https://github.com/Chocapikk/CVE-2024-34102), with a bash script to check all of our hosted sites to confirm the patch.

This repository is provided to allow store owners / hosts to confirm the patch is applied on stores. Within `check.bash` add domains to the `SITES` list.

[https://www.sdj.pw/posts/magento2-cosmic-sting-check/](https://www.sdj.pw/posts/magento2-cosmic-sting-check/)

[Online Validator https://cosmicsting.samdjames.uk/](https://cosmicsting.samdjames.uk/)

## Setup
```sh
# Create a python virtual environment for the project
python -m venv venv

# Activate virtual environment (pick appropriate below)
source venv/bin/activate # MacOS / Unix
venv\Scripts\activate    # Windows

# Install Requirements
pip install -r requirements.txt
```

## Usage
```sh
# Run the POC against a single store
./poc.py -u https://samdjames.uk

# To run the POC against multiple stores, first create txt file containing the list of sites seperated by a new line
# for example `sites/example.txt`. And pass it as the first positional argument of the ./z_validate script.
./z_validate sites/example.txt

# A very basic check monitoring stores for compromise
# Dumps all script src's to a file, and compares against the previous run.
./z_compromise_check sites/example.txt
```

