---
title: Hardware 
linktitle: 1 - Hardware Options
description: Options for SDR hardware and host computers
weight: 100
---

## Selecting a Software-Defined Radio (SDR)

ORCA is built upon the [USRP Hardware Driver](https://github.com/EttusResearch/uhd) (UHD).
As such, it is theoretically compatible with any [Ettus](https://www.ettus.com) SDR.
We have primarily tested with B and X series devices (B205mini and X310, in particular),
however most other Ettus SDRs should work with minor tweaks.

The basic capabilities of the two models we regularly use are detailed below:

| SDR              | Frequency Range (GHz) | Bandwidth (MHz) | Channels   | Mass (kg) | Approximate Cost (USD) |
|------------------|-----------------------|-----------------|------------|-----------|------------------------|
| [X310](https://www.ettus.com/all-products/x310-kit/) with [UBX160](https://www.ettus.com/all-products/ubx160/) | 0.01-6                | 200             | 2 TX, 2 RX | 1.7       | $14,0000               |
| [B205mini-i](https://www.ettus.com/all-products/usrp-b205mini-i/) | 0.07-6                | 56              | 1 TX, 1 RX | 0.024     | $1,600                 |

In general, we recommend B series devices for applications with constraints on
size, weight, power, or budget. When capabilities beyond the B series are needed,
we recommend the X series.

If no device in either series suits your needs, consider other Ettus SDRs. Most
should work with minor tweaks. The exception to note are E series devices, which 
include an embedded computer
running Linux. In theory, this code could be run on that embedded computer,
however the performance limitations would limit the use cases.

## Host Computer

Unless you choose an E series device (see caution above), you will also need a
computer to interface with the SDR. This computer is where the ORCA code will
run.

The capabilities of the computer can make a significant difference in the
system performance. The host computer must support an interface with enough
bandwidth for the samples you want to transfer and be able to store these
samples to an appropriate storage medium.

If you're not resource constrained, a modern laptop will provide more than
enough processing power, as long as it supports the interface you need. Keep in
mind that X-series SDRs need a 10 gigabit ethernet (10 GigE) interface to achieve maximum
sample rates. Few laptops natively support 10 GigE, however there are 
Thunderbolt adapters available. (Not all USB C ports support Thunderbolt and
it may not be available on low-end laptops.)

For an embedded solution, Raspberry Pi's are suitable for working with B series
devices. The performance of the Raspberry Pi 5 greatly exceeds the Raspberry Pi
4, likely due to the introduction of a new USB interface chip.

Some caution is advised with other single-board computers. Their performance will
likely be limited by their choice of USB controller chip.

For some examples of duty cycles achievable with various combinations of SDRs
and host computers, see the figure below. Note that actual performance will
depend on a variety of factors, including your exact configuration and the
speed of your storage medium.

{{% imgproc duty_cycle_comparison_with_pi5 Fit "800x400" %}}
Example results from running `error_code_late_command_sweep.py` on several
combinations of host computers and SDRs.
{{% /imgproc %}}

## MicroSD Card
Not all (micro) SD cards are the same. Speed and reliability can both vary a lot.

Especially if you plan to store your data to your MicroSD card, you don't want to
mess around with this. Don't use an SD card that's off-brand, questionably sourced
(i.e. possibly counterfeit), or used.

We use Samsung Pro Plus series MicroSD cards. There are other storage options too.
See [Other Storage Options](/docs/peregrine/payload/data-storage) for details. 

{{% pageinfo %}}
Next, [set up ORCA](/docs/radar/setupguide/2ORCAsetup) on your device.

{{% /pageinfo %}}