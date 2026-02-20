---
title: Data Storage Options
description: Options for how to store your radar data as its being recorded
weight: 110
---

There are three tested options for how to store your radar data, with various tradeoffs:

1. MicroSD card -- This is the *default* option that is assumed in the documentation.
2. External USB SSD or Flash Drive
3. NVMe SSD connected over PCIe interface (Pi 5 only)

### MicroSD card

This is the easiest option since it's built-in to the Raspberry Pi and requires no additional space or equipment.

MicroSD card quality varies significantly and counterfits are an issue. For this reason, purchasing from a reputable vendor is highly recommended.

We use [Samsung Pro Plus MicroSDXC cards](https://www.samsung.com/us/computing/memory-storage/memory-cards/pro-plus-adapter-microsdxc-512gb-mb-md512sa-am/), usually in 512 GB capacity.

You can find lots of online benchmarks of various MicroSD cards, such as [this one](https://www.jeffgeerling.com/blog/2019/raspberry-pi-microsd-card-performance-comparison-2019) and [this one](https://www.pidramble.com/wiki/benchmarks/microsd-cards).

There are two downsides to this approach:
1. Above 1 TB, MicroSD cards start to get quite expensive.
2. If you're storing data on the MicroSD card, it's not possible to use [`overlayroot` to protect](/docs/peregrine/payload/pi-sd-setup/#using-overlayroot-to-protect-the-file-system) the file system from corruption.

### External USB drives

External USB 3 SSDs or flash drives may be plugged into the USB 3.0 ports on the Pi and used as storage devices. We have used Samsung T7 Shield SSDs successfully in field deployments. The major advantage of this approach is that it is easy to swap out storage devices.

### NVMe SSD

Starting with the Pi 5, a PCIe port is exposed allowing for NVMe devices including SSDs to be added. We have succesfully used the [Pimoroni NVMe Base](https://shop.pimoroni.com/products/nvme-base?variant=41219587178579).

This is the highest speed and most reliable storage option. The configuration we've tested so far has kept the OS and radar code on the MicroSD card and used the SSD only for storage. It is, however, possible to [boot directly](https://www.jeffgeerling.com/blog/2023/nvme-ssd-boot-raspberry-pi-5) from an NVMe SSD, though this configuration has not been tested with ORCA.
