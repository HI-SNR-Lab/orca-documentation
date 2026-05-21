---
title: Runtime overview
linkTitle: 3 - Runtime Overview
description: Overview of the code's architecture
weight: 10
---

## Conda environment setup

All of the required dependencies can be installed as a conda environment using
the `environment.yaml` file in the repository. More instructions can be found
in the [README](https://github.com/radioglaciology/uhd_radar/tree/main?tab=readme-ov-file#configuring-your-environment)
file.

## Startup scripts

The X series devices require some initial network configuration. For convenience,
a [startup script](https://github.com/radioglaciology/uhd_radar/blob/main/x310_startup.sh)
is provided to automate this setup. You may need to tweak this file to your setup.

## Runner scripts

The basic steps required to run the radar are:

1. Build the C++ code
2. Generate a chirp file to transmit based on your configuration
3. Run the compiled radar code
4. Move the collected data to an appropriate location

The main interface for running the radar code is through `run.py`, a Python
script designed to automate the above process. This script is run as follows:

```
python run.py config/my_radar_configuration.yaml
```

At the end of the data collection, data will be saved with the current date
to a location specified in the [YAML config file](/docs/radar/sdr-interface/config).

Generally, three files are saved:

* `YYYYMMDD_hhmmss_rx_samps.bin` - This is a binary file containing the raw 
samples recorded the SDR. Note that this file is not interpretable unless you
also have the config file used.
* `YYYYMMDD_hhmmss_config.yaml` - This is the YAML config file passed to `run.py`.
It defines all parameters of the data collection, allowing for the `rx_samps.bin`
file to be interpreted and processed.
* `YYYYMMDD_hhmmss_uhd_stdout.log` - This is a text file containing the output
of running the radar code. This is helpful for debugging and also contains a log
of any errors encountered, which may be required to reconstruct the timing of
each recording.

More details on the files stored and how these can be re-processed into a Zarr
file are on the [file formats](/docs/radar/postprocessing/files/) page.

Note that there are also settings available to break `rx_samps.bin` into multiple
files as needed.

## SDR interface code

For performance reasons, the code directly interfacing with the SDR is written
in C++. This code is all located in the `sdr/` directory of the repository.

The main radar code is contained in `main.cpp` (with some SDR setup code located
in `rf_settings.cpp`). The radar code runs in two threads, as shown in the
figure below.


{{% imgproc code_diagram Fit 500x1200%}}
General architecture of the ORCA code
{{% /imgproc %}}

One thread is responsible for scheduling
[timed commands](https://kb.ettus.com/Synchronizing_USRP_Events_Using_Timed_Commands_in_UHD)
that are enqueued into FIFO queues within the SDR's FPGA.

The other thead is responsible for pulling received samples from the SDR and
writing them to a file on the host computer.

For a more complete overview, please refer to our paper:

{{% readfile "/docs/tgrs_citation.md" %}}