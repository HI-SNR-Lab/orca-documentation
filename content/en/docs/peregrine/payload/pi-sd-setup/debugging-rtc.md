---
title: "Debugging: Real-Time Clocks (RTC)"
description: RTC choices and possible solutions to RTC issues 
weight: 100
---

A real-time clock (RTC) is a small device equipped with a crystal oscillator and
a battery that is responsible for keeping track of the current time, even while
your computer (or Raspberry Pi) is powered off.

The "Payload Enclosure Divider" includes a [PCF8523](https://www.nxp.com/docs/en/data-sheet/PCF8523.pdf)
RTC and a holder for a CR1220 coin cell battery. The provided `user-config` file
should automatically set this up. As long as you provide internet access to
the Pi once, it will automatically synchronize the RTC with a network time server
and everything will just work.

### Tell me more about the PCF8523 and how to use it

Adafruit makes a great breakout for the same chip [available here](https://www.adafruit.com/product/5189).

They also have a great [tutorial on setting up various RTCs with the Pi](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all).

### My Pi 5 already has an RTC built-in, right?

Yes, there is. [Documentation for the built-in RTC is here.](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#real-time-clock-rtc)

The built-in RTC still requires adding a _rechargable_ lithium manganese battery
to the Pi's J5 connector. Charging of this battery is disabled by default and
must be manually enabled.

In theory, you should be able to add the official Pi RTC battery, follow the
official instructions to enable charging, and everything should work.

### I have a Pi 5 but still want to use

