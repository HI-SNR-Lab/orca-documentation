---
title: 6 - Testing Layout
description: How to conduct testing using ORCA to confirm that the current setup works as expected.
weight: 10
---

## Indoor Testing

While indoors, make sure **not** to transmit any signals with the antenna. Only transmit into the spectrum analyzer or in a loopback configuration to the SDR. 

**Before doing any testing in a loopback configuration, use the spectrum analyzer to confirm that the transmitted power is less than the maximum input power the SDR can handle.** 

When connecting any SMA cable, make sure to hold the cable and connection point still while you connect it so that the cable **does not spin** as you tighten the nut, as this can cause damage to the pin. Tighten the nut using the SMA torque wrench (the wrench will bend when the proper tightness is reached). 

### Spectrum Analyzer Test
To test the program with the spectrum analyzer, you will need the following equipment: 
* b205mini SDR 
* USB 3.0 Micro B cable (connecting SDR to Pi) 
* Raspberry Pi 5 
* Raspberry Pi 5 Power Supply (USB C) 
* Ethernet cable (connecting Pi to Laptop) 
* Ethernet to USB C adapter (if your laptop doesn't have ethernet) 
* 30 dB inline attenuator 
* 2 SMA male-male cables 
* SMA female-female adapter (or replace one of the male-male cables with a male-female cable) 
* SMA torque wrench 
* SMA female to N-Type male adapter (probably plugged into the spectrum analyzer RF Input port already) 
* Spectrum Analyzer (Rigol DSA832-TG) 
* 50 Ohm Load (Found in the Calibration Kit F604MS) 

**Process**
1. Ensure the blue ESD mat is properly grounded, and there are no food or drinks nearby. 
2. Carefully take the 50 Ohm Load out of the calibration kit box. Be very careful while handling this piece of equipment.  
3. Connect 50 Ohm Load to the “RX2” port on the SDR, ensuring that the load does not spin while the nut is being tightened. Tighten it using the torque wrench. 
4. Connect this cable to the SMA female-female adapter. 
5. Connect the SMA female-female adapter to the “IN” port on the 30 dB attenuator. 
6. Connect the other SMA cable to the “OUT” port on the 30 dB attenuator.  
7. Connect this SMA cable to the SMA female to N-Type adapter. 
8. Connect the SMA female to N-Type adapter to the “RF Input” port on the spectrum analyzer if it is not already connected. Take special care that the adapter does not spin while connecting it to this port. 
9. Turn on the spectrum analyzer.
10. Set the Spectrum Analyzer's frequency to the chirps' configured center frequency. 
11. Set the span of the spectrum analyzer to a bandwidth that allows you to see your full chirp in detail. 
12. Configure your spectrum analyzer to see the maximum value when sampled. 
13. Follow the steps in the sections above to connect your laptop to the Pi and get all the code ready to run on the Pi. 
14. Plug the USB 3.0 Micro B cable into one of the blue USB ports on the Pi and plug the other end into the SDR. 
15. Follow the Running the Code section below on how to run the program. 
16. When the code is running, you should see the transmissions appear on the spectrum analyzer. To see the peak transmitted power, press “Peak”. Ensure that this value is less than the SDR’s max input power before doing any loopback or outdoor testing. 
17. Since the SDR is not receiving any samples, you will see receiver errors printed to `uhd_stdout.log`, and `rx_samps.bin` will be empty.

### Loopback Test 

To get any actual data from the SDR, we must both transmit and receive signals by connecting the SDR to itself in a loopback configuration. 

**Before running the program in this configuration, make sure that you have tested your current code and config settings with the spectrum analyzer method above, and that the peak power is less than the SDR’s max input power (-15 dBm)!** 

**When connecting the b205mini to itself, you should always use a 30 dBm attenuator!**

1. Follow the steps in the Spectrum Analyzer section above to set up the hardware and test it with the spectrum analyzer. Confirm that the program works and the peak power is less than -15dBm. 
2. Stop all transmissions, and do not transmit again until everything has been reconnected. You can unplug the SDR from the Pi to ensure this cannot happen. 
3. Disconnect the SMA cable from the adapter on the spectrum analyzer. 
4. Carefully disconnect the 50 Ohm Load and place it back in the box. 
5. Connect the SMA cable to the “RX2” port on the SDR. 
6. Plug the SDR back into the Pi if you disconnected it previously. 
7. Follow the Running the Code section below to run the program.

## Running the Code: 
Now that you’re connected to the Pi and have hardware set up, you can run the code with the following commands: 

1. `cd uhd_radar/` 
2. `conda activate uhd`
3. Check your config settings are set correctly with `nano config/<your-file>.yaml` 
    - If you are using the B205-mini, make sure the following values in `RF0` (not RF1) section are set: 
        - `tx_gain` should **not** exceed ~80 dB
        - `rx_gain` should **not** exceed 76 dB
        - `tx_ant` should be set to `"TX/RX"`
        - `rx_ant` should be set to `"RX2"`
        - `transmit` should be set to `True`
4. run `make hardware-test` 
5. run `python run.py config/<your-file>.yaml` 
    - If you have `num_pulses` set to `-1`, then you must stop the program with `Ctrl+C`
6. To view the output data, transfer the desired data files to a laptop, ensure the `PLOT` section has been copied to the config file (it can be found in `synthetic-config.yaml`) and update the parameters in that section to match the names of the trial you wish to view
7. Plot the output with `python postprocessing/plot_samples.py data/<timestamp>_config.yaml` 


