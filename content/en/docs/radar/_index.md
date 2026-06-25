---
title: ORCA Software-Defined Radar
linkTitle: ORCA Software-Defined Radar Guide
#description: Details about the Peregrine UAS
weight: 1
menu: {main: {weight: 1, pre: "<i class='fa-solid fa-gears'></i>"}}
---

{{% pageinfo %}}
For a general overview of the ORCA system, we highly recommend reading through
our publication:

{{% readfile "/docs/tgrs_citation.md" %}}

{{% /pageinfo %}}

Code for ORCA can be found on the [Github Page](https://github.com/HI-SNR-Lab/uhd_radar), which contains additional details about downloading and testing ORCA on the radios that are currently available.

This guide is divided into three parts to help set up and understand ORCA. ORCA uses a computer and a software-defined radio (SDR) to create a functioning radar. As the architecture is currently configured, the computer is a Raspberry Pi, and the SDR is an Ettus radio. Current work is being done to implement ORCA on a Xilinx board, which would act as both a computer and SDR.


<div style="text-align: center; margin: 40px 0;">
    <img src="/docs/radar/pi-sd-setup/photos/computer-sdr.png" alt="Computer to SDR Basic Implementation" width="40%">
</div>

<!-- ![Computer to SDR Very Basic Implementation](/docs/radar/pi-sd-setup/photos/computer-sdr.png) -->

[Setup Guide for Beginners (do i remove beginners)](/docs/radar/setupguide) is a guide to set up your own ORCA and SDR system from scratch. Most likely you will want to start here. 

<!-- [Hardware Setup](/docs/radar/pi-sd-setup) details how to connect to the computer and software defined radio, which is currently a Raspberry Pi.

[Radar Code](/docs/radar/sdr-interface/) covers everything about the code that runs while the radar is actively collecting data. 

[Postprocessing](/docs/radar/postprocessing/) section explains how data is saved and explains the basic processing scripts that we provide. -->
