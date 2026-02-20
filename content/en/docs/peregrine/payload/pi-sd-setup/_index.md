---
title: Raspberry Pi Setup
#description: 
weight: 100
---

In order to standardize between units, much of the Pi setup is automated or
semi-automated. This guide will walk you through the steps of setting up
your Pi the way we do. Along the way, there are also links for more information
on how to customize this setup. This is an area where you will almost certainly
need to customize some aspects of the setup.

## Initial setup with cloud-init

Setup of the Raspberry Pi is semi-automated using [cloud-init](https://cloudinit.readthedocs.io/en/latest/).

### Cloud-init customization

The cloud-init setup is controlled by two files: `user-data` and `network-config`.
(You'll use these files a couple of steps down.)

Examples of each are shown below, but you will likely need to modify these to suit
your purpose. We have pages on how to customize
[user-data]({{< ref "user-data-config" >}}) and
[network-config]({{< ref "pi-internet" >}}).

#### user-data Example
{{< readfile file="/static/cloud-init/user-data" code="true" lang="yaml" >}}

### network-config Example
{{< readfile file="/static/cloud-init/network-config" code="true" lang="yaml" >}}

## Imaging your Pi

To start, download the Raspberry Pi Imager tool (or use your preferred software
for imaging SD cards). On Ubuntu, you can install it like this:

```
sudo apt install rpi-imager
```

For other operating systems, see the [website](https://www.raspberrypi.com/software/).

{{% alert title="Note on selecting a microSD card" color="info" %}}
Not all (micro) SD cards are the same. Speed and reliability can both vary a lot.

Especially if you plan to store your data to your MicroSD card, you don't want to
mess around with this. Don't use an SD card that's off-brand, questionably sourced
(i.e. possibly counterfeit), or used.

We use Samsung Pro Plus series MicroSD cards. There are other storage options too.
See [Other Storage Options](/docs/peregrine/payload/data-storage) for details.
{{% /alert %}}

Launch Imager. After clicking on "Choose OS," navigate through the general purpose
category to find `Ubuntu Server 22.04.xx LTS 64-bit`. 64-bit is important -- 32-bit
will not work.

{{% imgproc pi-os Fit "800x400" %}}
You want Ubuntu Server 22.04 LTS 64-bit.
{{% /imgproc %}}

Insert your MicroSD card and select it as the location to write to.

After imaging is complete, you will see two drives mounted: `writable` and
`system-boot`.

## Copying cloud-init config files

After customizing the `user-data` and `network-config` files (see above),
copy `user-data` and `network-config` to the `system-boot` volume, replacing the
existing files.

Eject the microSD and put it back in the Pi.

## Running cloud-init

{{% alert title="Your Pi needs an internet connection for this part" color="info" %}}
Make sure you Pi will have access to the internet before you begin this part.
See the [networking page]({{< ref "pi-internet" >}}) for information.
{{% /alert %}}

Power up the Pi and wait for cloud-init to run.

Within about a minute, your Pi should connect to whatever network interface(s)
are described in `network-config` and you should be able to find it on the
network. If you setup some sort of key-based authentication (such as by
importing a key from GitHub), it may take an extra couple of minutes for
this to be ready.

After the network setup is complete, you should be able to login over SSH.

For instructions on SSH-ing into your Pi, see [here]({{< ref "connect-to-pi" >}}).
In particular, please note that you need to have SSH agent forwarding working.
Instructions for this are on that page.

When you first login, cloud-init may not have finished running. To check the status, run:

```
cloud-init status --long
```

There are also logs in `/var/log/cloud-init-output.log`.

To keep an eye on the entire process, you can run:

```
watch "cloud-init status --long && tail -n 10 /var/log/cloud-init-output.log"
```

Expect this process to take a few minutes to complete.

## Running initial_setup.sh

After the cloud-init process is complete, you'll also need to run
`initial_setup.sh`:

`./initial_setup.sh`

This will log to `/home/ubuntu/initial_setup_output.log`. It may take around 10
minutes to complete. It will automatically reboot your Pi at the end. If you
don't want this, feel free to comment out the last line.

## Setting up the logger service

More details on the logging service will eventually be [here]({{< ref "logger-service" >}}).

For now, if you're building a Peregrine system, the default setup should be fine.

If you're building Eyas, first run this command to create a place for logs:

```
mkdir /media/ssd/logger
```

And then modify the last line of `/home/ubuntu/uav_radar_logger/logger_service.sh`
to look like this:

```
python -u logger.py --shutdown-voltage 11.8 --log-dir /media/ssd/logger/
```

Replacing `11.8` with an appropriate threshold (in volts) at which to shutdown.

## Setting up the radar service

More details on the radar service will eventually be [here]({{< ref "radar-service" >}}).

For now, if you're building a Peregrine system, the default setup should be fine.

If you're building Eyas, run these commands to create a location for logging data
and update the default configuration:

```
mkdir /media/ssd/radar
cd /home/ubuntu/uhd_radar/config
mv default.yaml default-old.yaml
cp default-eyas.yaml default.yaml
```

## Using overlayroot to protect the file system

Let's take a quick step back and talk about the problem before we talk about
(perhaps drastic) solutions:

[MicroSD card corruption](https://hackaday.com/2022/03/09/raspberry-pi-and-the-story-of-sd-card-corruption/)
is an ongoing challenge for any device (such as the Pi) that boots from a
MicroSD card. Most cases can be traced to either (a) junk MicroSD cards or
(b) sudden power loss during a write operation.

You can mostly avoid problem (a) by carefully sourcing your MicroSD cards. If
you're considering saving $20 by buying an off-brand MicroSD card or, worse, 
a possible fake, don't do it.

Sudden power loss is harder to completely guard against. Ideally, you want to
shutdown your Pi before removing power. This can be done by SSH-ing into it and 
running `sudo shutdown -h now` and waiting about a minute. If you use our
radar systemd service, you can also perform a safe shutdown by pressing and
holding the button for 5 seconds, waiting for the light to turn off, and then
giving it about a minute to fully shut down.

For Peregrine, this should all be good enough.

For Eyas and other longer-term installations, the risk of a battery discharging
faster than expected is relatively high.

The first line of defense is the automatic shutdown provided by the logger
service that will safely shut everything down when the battery voltage gets too
low.

If you have a separate data storage device, such as an external USB-connected SSD,
you can go a step further and make your Pi's MicroSD card read-only.

A utility called `overlayroot` (which uses [OverlayFS](https://docs.kernel.org/filesystems/overlayfs.html))
can be used to make the root filesystem read-only and create an "overlay filesystem"
stored only in RAM. This means that all changes to the MicroSD card file system
are temporary and are lost upon reboot.

This is great for keeping a standardized configuration, but you need to be aware
that this means most log files are lost on reboot, any config files on the SD
card are lost on reboot, and all radar data you want to keep around must be stored
to your external storage device.

You can read
[a more detailed tutorial about Overlayroot here](https://rex.writeas.com/use-overlay-filesystem-on-ubuntu).

**If you're going to do this, be sure that you've tested your setup in advance
so you know if the data you want to keep is being stored.**

### Enabling Overlayroot

If you still want to set this up, it's quite easy to enable.

Simply edit the last line of `/etc/overlayroot.conf` to this:

```
overlayroot="tmpfs:recurse=0"
```

`tmpfs` specifies that we want to use a RAM-based filesystem to store the "overlay"
part of the filesystem. `recurse=0` says that we want to apply this only to the
`/` mount and not to other mounts below that.

(You need to edit this file as root. For example: `sudo vim /etc/overlayroot.conf`)

### Disabling Overlayroot

You can temporarily re-mount the root filesystem to edit things using the
built-in utility:

```
sudo overlayroot-chroot
```

To exit, just type `exit`.

If you want to permenantly disable it, just edit the last line of `/etc/overlayroot.conf`
back to:

```
overlayroot=""
```

and reboot.