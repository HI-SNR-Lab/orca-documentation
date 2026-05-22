---
title: Timing and timestamping
linkTitle: Timestamps
description: How recorded samples are timestamped and options for synchronization
weight: 100
---

{{% pageinfo %}}
Timestamping of received data is relatively basic and not yet suitable for
high-precision applications. This page describes the basics as currently implemented.

There is significant room to improve on ORCA here. USRP devices are capable of
multiple means of synchronization between devices that could be used to provide
better timestamping.
{{% /pageinfo %}}



## Relative timing of samples

Transmit and receive events are scheduled as
[timed commands](https://kb.ettus.com/Synchronizing_USRP_Events_Using_Timed_Commands_in_UHD).
Generally, bursts of samples are recorded at intervals specified by `pulse_rep_int`.

When an error occurs, extra time is added to allow the system to catch up. The
amount of time added is configured by the `error_recovery_time` parameter. When
time is added, a message is printed to `stdout` with the chirp number and the
amount of time added, such as the following:

```
[1691434273.020] 	[TX] (Chirp 975541) time_offset increased by 0.0016
```

Note that due to the enqueueing of commands, multiple errors may occur before the
next set of commands is enqueued with a time offset. If more than one error occurs,
the time will be offset by `number of errors * error_recovery_time`.

These output messages are read during the Zarr file creation process in order to
provide a corrected slow time record.

{{% alert title="Older versions" color="info" %}}
Older versions of ORCA did not print out the time offset messages and had hard-coded
error recovery time. When this situation is detected (by the combination of a
non-zero number of logged errors but no time offset messages), the time offset is
estimated based on the starting and ending system clock, rounded to the nearest
multiple of `pulse_rep_int`.
{{% /alert %}}

## Timestamping samples

ORCA currently assumes that the SDR clock is useful to relative timing only and
relies on the _host computer_ clock to provide a starting timestamp. When using
the [run.py interface]({{< ref "/docs/radar/pi-sd-setup/code#runner-scripts" >}}),
`stdout` output is logged with a Unix timestamp from the host computer. The
timestamp on the starting message (plus any specified `time_offset` in the config
file) is used to provide the absolute time of the first transmission.

This relies upon the system clock being set accurately and should never be assumed
to provide sub-second accuracy.

## Accessing timestamps in Xarray

The default coordiantes of the radar DataArray are `sample_idx` and `pulse_idx`.
These correspond to the fast time and slow time indices of the as-recorded data.

Considering `pulse_idx` this means, for example, that if `num_presums` is 10,
then there are 10 chirps transmitted and received for each index of `pulse_idx`.
Similarly, any errors are ignored in counting `pulse_idx`.

The additional data variables `chirp_sequence_idx`, `slow_time`, and `timestamp`
may be used if other information is needed. They are as follows:

* `chirp_sequence_idx` refers to the index as tracked by the SDR of the first chirp
included in the associated data recording. With no errors,
`chirp_sequence_idx = num_presums * pulse_idx`.
* `slow_time` refers to the relative time (in seconds) of the start of the first
chirp included in the assocaited data recording.
* `timestamp` is an `np.datetime64` series equal to `slow_time + start timestamp`