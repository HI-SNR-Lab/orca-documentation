---
title: Network Configuration
linkTitle: 5 - Network Setup
description: How to configure the netplan for when the Raspberry Pi initially boots up
weight: 10
---

# Setting up network interfaces

## With cloud-init (first-time setup)

The preferred way to setup network interfaces is by providing them in the
`network-config` file read by [cloud-init when first setting up the Pi]({{< ref "pi-sd-setup" >}}).

An example is shown below:

{{< readfile file="/static/cloud-init/network-config" code="true" lang="yaml" >}}

The above configuration sets up a static IP over the ethernet interface. It
also configures `192.168.11.1` as the default gateway. This allows for sharing
an internet connection from a computer over this interface if desired.

The configuration also provides an SSID and password for a WiFi network. In practice,
we configure this to the settings for a phone hotspot that can be used to get
internet when WiFi is not otherwise available. This is also a simpler setup for
getting the Pi on the internet when needed.

## Reconfiguring with netplan

By default, network interfaces are configured with netplan. See
[the netplan documentation](https://netplan.readthedocs.io/en/stable/examples/)
for more details.


By default, the cloud-init script sets up a static IP of `192.168.11.137`, but
you could choose to configure this to something different for each payload box.

Our usual way of connecting is by plugging an ethernet cable into the Pi and
connecting it to a laptop. You can read about
[all the networking options here]({{< ref "network" >}}).
