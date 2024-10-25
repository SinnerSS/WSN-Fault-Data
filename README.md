# WSN-Fault-Data

A curated dataset of temperature measurements from the NASA MERRA-2 model, designed for simulating and analyzing faults in Wireless Sensor Networks (WSN).

## Dataset Overview

The repository contains temperature data collected from 5 distinct global locations, with 5 temperature measurement points per location. Two separate datasets are provided:

- **Daily Dataset**: 
  - Period: January 1, 2019 - December 31, 2023
  - Interval: 1 day
  
- **Hourly Dataset**:
  - Period: January 1, 2023 - December 31, 2023
  - Interval: 1 hour

## Installation

### Option 1: Direct Download
You can directly download the `.csv` files from the `/data` directory on GitHub.

### Option 2: Sparse Checkout
To download only the data files using git sparse-checkout:

```bash
# Create and enter directory
mkdir WSN-Fault-Data && cd WSN-Fault-Data

# Initialize git and set remote
git init
git remote add origin https://github.com/SinnerSS/WSN-Fault-Data

# Configure sparse-checkout
git sparse-checkout init
git sparse-checkout set data

# Pull data
git pull origin main
```

### Option 3: Process Raw Data
You can process the raw data yourself using the `.txt` files from the `raw` directory. Data can be downloaded using wget from NASA GES DISC:

For detailed instructions, visit: [How to Access GES DISC Data Using wget and curl](https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Access%20GES%20DISC%20Data%20Using%20wget%20and%20curl)
Data%20Using%20wget%20and%20curl 

## Data Source
This dataset uses temperature data from the NASA Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2) model:

###Daily Data

- **Dataset**: MERRA-2 statD_2d_slv_Nx (M2T1NXSLV v5.12.4)
- **Variable**: T2MMean (2-meter air temperature mean)
- **DOI**: 10.5067/9SC1VNTWGWV3

###Hourly Data

- **Dataset**: MERRA-2 inst1_2d_asm_Nx (M2T1NXSLV v5.12.4)
- **Variable**: T2M (2-meter air temperature)
- **DOI**: 10.5067/3Z173KIE2TPD
