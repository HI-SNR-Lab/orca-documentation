---
title: Raspberry Pi Setup 
linktitle: 2 - Raspberry Pi Setup
description: Imaging your Pi and Editing Configuration Files
weight: 100
---
<link rel="stylesheet" href="../style.css">

In order to standardize between units, much of the Pi setup is automated or semi-automated. This guide will walk you through the steps of setting up your Pi the way we do. Along the way, there are also links for more information on how to customize this setup. This is an area where you will almost certainly need to customize some aspects of the setup.

## Imaging your Pi
To start, download the Raspberry Pi Imager tool (or use your preferred software
for imaging SD cards). Imaging is basically giving the Raspberry Pi an operating system. On Ubuntu, you can install it like this:

```
sudo apt install rpi-imager
```

For other operating systems, download the tool from [here](https://www.raspberrypi.com/software/).

{{% alert title="" color="info" %}}
Remember to choose your microSD card carefully as mentioned in [hardware options](/docs/radar/setupguide/1hardware)
{{% /alert %}}

1. Launcher the imager
2. Select what version of Raspberry Pi you are using
3. Under "OS" select "Other general-purpose OS"
4. Select Ubuntu
5. Scroll until you find `Ubuntu Server 24.04.xx LTS (64-bit)`. Make sure you get 64-bit, 32-bit will not work. Also make sure that the Raspberry Pi you are using is supported. 

{{% imgproc OS-version-image Fit "800x400" %}}
You want Ubuntu Server 24.04 LTS 64-bit and make sure your Pi is supported as shown in the highlight
{{% /imgproc %}}
6. Insert your SD card if you haven't already done so, and select it
7. Skip customization, we will create our own user-data file to insert
8. Image the SD card

After imaging is complete, you should see a `system-boot` drive and maybe a `writable` drive. `system-boot` is more important. 

{{% alert title="Can't find system-boot?" color="info" %}}
If you see a different drive from the SD card that tells you to format it in order to read it, do not format it. The following information is likely Windows specific. If you can't see the `system-boot` drive, it is likely because it wasn't assigned a letter. You need admin privliages to fix this. Hit `WIN + X` and select "Disk Manager". You will see the `system-boot` drive there, it just doesn't have a letter. Right click on it and assign a letter. Click "add" on the pop up and assign it a letter. The drive should now be visible in your file explorer.
{{% /alert %}}

## Cloud-init
Setup of the Raspberry Pi is semi-automated using [cloud-init](https://cloudinit.readthedocs.io/en/latest/).

### Cloud-init customization

The cloud-init setup is controlled by two files: `user-data` and `network-config`.
(You'll use these files a couple of steps down.)

Examples of each are shown below, but you will likely need to modify these to suit
your purpose. We have pages on how to customize
[network-config](/docs/radar/setupguide/2RaspPi/1networkconfig) and [user-data](/docs/radar/setupguide/2RaspPi/2userdataconfig).

#### user-data Example
{{< readfile file="/static/cloud-init/user-data" code="true" lang="yaml" >}}

### network-config Example
{{< readfile file="/static/cloud-init/network-config" code="true" lang="yaml" >}}

### network-config Example for Laptop Mobile Hotspot and Possibly Normal Wifi
{{< readfile file="/static/cloud-init/network-config-mobile-hotspot-example" code="true" lang="yaml" >}}

{{% alert title="" color="info" %}}
If your wifi SSID or password has slashes, it might freak the Raspberry Pi out and the network-config won't run properly. 
{{% /alert %}}

After you edit the user-data and network-config files and add them to your SD card. You can now put the card back into the Pi.

{{% pageinfo %}}
Next, read on how to power on and [connect to the pi](/docs/radar/setupguide/3connectingPi).

{{% /pageinfo %}}