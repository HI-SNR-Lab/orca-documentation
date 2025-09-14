---
title: SORA Sled-Towed Radar
linkTitle: SORA
description: Details about the ground-based reconfiguration of Peregrine
#menu: {main: {weight: 100, pre: "<i class='fa-solid fa-sleigh'></i>"}}
weight: 100
---

{{% pageinfo %}}
SORA (Sledbord ORCA Reconfigured from Airborne) is a ground-based enclosure for the Peregrine radar payload that
has space to host a larger power amplifier. It was initially designed to be a testing platform for payloads for
larger UAVs, but it can also be used as a standalone ground-based system.

It can be paired with any antennas, but the MAPPERR antennas make a great choice.

Previously known as "Peregrine+"
{{% /pageinfo %}}

{{% imgproc sora_insides_bench Fit "800x400" %}}
SORA enclosure on the bench
{{% /imgproc %}}

## RF Frontend

{{% imgproc peregrine_plus_rf_frontend Fit "800x400" %}}
Block diagram of the RF components in the SORA RF frontend. Maximum power levels under three scenarios (nominal, worst-case, and an example expected bed return) are shown. The system is designed to be modular, so feel free to swap out as needed.
{{% /imgproc %}}


## Bill of Materials

A complete bill of materials for SORA is in [this Google Sheet](https://docs.google.com/spreadsheets/d/1dFItvJ4mGw7Axdo4Iq9m_65ks9YspEahcemvucNRllk/edit?usp=sharing), embedded below. The first tab has the Peregine payload enclosure BOM. The SORA tab has the parts specific to this enclosure.

Some parts are custom made. See the [Custom Parts]({{< ref "custom-parts.md" >}}) page for suggestions on how to build these yourself or source them from reliable vendors. Design files for these parts are available in the [Peregrine Hardware repository](https://github.com/thomasteisberg/peregrine_hardware).

{{% iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSJbgsZBh6xJ8d5_O48yUdmh09coE1oZ8njQWZqQKYorwuMoUEFA6LCj9P5QiVQtoCGBCOOl3b1RTjY/pubhtml?widget=true&amp;headers=false" style="min-height: 40vh;" %}}



## Power amplifier power mounting

The power supply for the power amplifier mounts under the power amplifier tray. It looks like this without the rest installed:

{{% imgproc sora_pa_power_mounting Fit "800x400" %}}
The power supply for the power amplifier shown without the power amplifier tray covering it.
{{% /imgproc %}}