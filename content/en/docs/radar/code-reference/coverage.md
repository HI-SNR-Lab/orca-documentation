---
title: Documentation coverage
linkTitle: Documentation coverage
description: Which functions in the ORCA code have a comment that Doxygen can show
weight: 10
---

<!-- Written by doxygen/generate_api_docs.py. Do not edit by hand: the next run overwrites it. -->

Generated from `uhd_radar` commit 6d75349 (2026-10-30) with Doxygen 1.9.8.

A function counts as documented when Doxygen found a description for it. Doxygen only reads comments written in its own format, so an ordinary `//` or `#` comment does not count. The format is described under "Doxygen Requirements" in the [uhd_radar style guide](https://github.com/HI-SNR-Lab/uhd_radar/blob/main/STYLEGUIDE.md).

**Summary:** 31 of 132 functions (23%) have a description. Test files are in the table but not in this count.

| File | Documented | Functions | Coverage |
|---|---|---|---|
| manager/uav_payload_manager.py | 0 | 9 | 0% |
| postprocessing/Geostacking.py | 3 | 4 | 75% |
| postprocessing/auto_amplification.py | 0 | 1 | 0% |
| postprocessing/gps_processing.py | 0 | 2 | 0% |
| postprocessing/permanent_storage.py | 1 | 1 | 100% |
| postprocessing/plot_dask.py | 0 | 1 | 0% |
| postprocessing/processing.py | 0 | 12 | 0% |
| postprocessing/processing_dask.py | 7 | 8 | 88% |
| postprocessing/save_data.py | 0 | 1 | 0% |
| postprocessing/test_scripts/loopback_testing.py | 5 | 9 | 56% |
| preprocessing/generate_chirp.py | 2 | 2 | 100% |
| run.py | 0 | 8 | 0% |
| sdr/chirp.cpp | 2 | 15 | 13% |
| sdr/gps_test.cpp | 0 | 4 | 0% |
| sdr/main.cpp | 7 | 10 | 70% |
| sdr/pseudorandom_phase.cpp | 0 | 2 | 0% |
| sdr/pseudorandom_phase_to_file.cpp | 0 | 1 | 0% |
| sdr/rf_settings.cpp | 3 | 3 | 100% |
| sdr/sdr.cpp | 4 | 46 | 9% |
| sdr/utils.cpp | 2 | 2 | 100% |
| tests/error_code_late_command_sweep.py | 0 | 5 | 0% |
| tests/preprocessing/test_generate_chirp.py | 1 | 1 | 100% |
| tests/sdr/test_chirp.cpp | 5 | 5 | 100% |
| tests/sdr/test_pseudorandom_phase.cpp | 0 | 3 | 0% |
| tests/sdr/test_sdr.cpp | 9 | 18 | 50% |
| tests/sdr/test_utils.cpp | 0 | 2 | 0% |
| **All files** | 51 | 175 | 29% |

## Functions without a description

Test files are left out of this list.

### manager/uav_payload_manager.py

- `button_hold`
- `button_press`
- `error_and_quit`
- `log_output_from_usrp`
- `run_and_fail_on_nonzero`
- `signal_handler`
- `start_recording`
- `stop_recording`
- `update_led_state`

### postprocessing/Geostacking.py

- `stack`

### postprocessing/auto_amplification.py

- `sigint_handler`

### postprocessing/gps_processing.py

- `extract_locations_from_gpspipe`
- `parse_line`

### postprocessing/plot_dask.py

- `plot_radargram`

### postprocessing/processing.py

- `extractErrorsFromLog`
- `extractSig`
- `findDirectPath`
- `findEcho`
- `getSNR`
- `load_config`
- `load_radar_data`
- `loadSamplesFromFile`
- `plotChirpVsSample`
- `plotChirpVsTime`
- `pulse_compress`
- `stack`

### postprocessing/processing_dask.py

- `invert_phase_dithering`

### postprocessing/save_data.py

- `save_data`

### run.py

- `RadarProcessRunner.__init__`
- `RadarProcessRunner.process_usrp_output`
- `RadarProcessRunner.run`
- `RadarProcessRunner.save_from_queue`
- `RadarProcessRunner.setup`
- `RadarProcessRunner.stop`
- `RadarProcessRunner.wait`
- `sigint_handler`

### sdr/chirp.cpp

- `Chirp::getMaxChirpsPerFile`
- `Chirp::getNumPresums`
- `Chirp::getNumPulses`
- `Chirp::getPhaseDither`
- `Chirp::getPulseRepInt`
- `Chirp::getRxDuration`
- `Chirp::getTimeOffset`
- `Chirp::getTrOffTrail`
- `Chirp::getTrOnLead`
- `Chirp::getTxDuration`
- `Chirp::getTxLead`
- `Chirp::setMaxChirpsPerFile`
- `Chirp::setTimeOffset`

### sdr/gps_test.cpp

- `configureNMEAMessages`
- `configureRate`
- `main`
- `sendUBX`

### sdr/main.cpp

- `sig_int_handler`
- `transmit_worker`
- `UHD_SAFE_MAIN`

### sdr/pseudorandom_phase.cpp

- `get_next_n_phases`
- `get_next_phase`

### sdr/pseudorandom_phase_to_file.cpp

- `main`

### sdr/sdr.cpp

- `Sdr::check10MhzLock`
- `Sdr::checkAndSetTime`
- `Sdr::detectChannels`
- `Sdr::getAmpGpioMask`
- `Sdr::getAtrControl`
- `Sdr::getAtrMasks`
- `Sdr::getBw`
- `Sdr::getClkRate`
- `Sdr::getClkRef`
- `Sdr::getCpuFormat`
- `Sdr::getDeviceArgs`
- `Sdr::getFreq`
- `Sdr::getGpioBank`
- `Sdr::getGpioDdr`
- `Sdr::getOtwFormat`
- `Sdr::getPwrAmpPin`
- `Sdr::getRefOutInt`
- `Sdr::getRf0`
- `Sdr::getRf1`
- `Sdr::getRxAnt`
- `Sdr::getRxChannelNums`
- `Sdr::getRxChannels`
- `Sdr::getRxChannelStrings`
- `Sdr::getRxGain`
- `Sdr::getRxRate`
- `Sdr::getRxStream`
- `Sdr::getSubdev`
- `Sdr::getTransmit`
- `Sdr::getTxAnt`
- `Sdr::getTxChannelNums`
- `Sdr::getTxChannels`
- `Sdr::getTxChannelStrings`
- `Sdr::getTxGain`
- `Sdr::getTxRate`
- `Sdr::getTxStream`
- `Sdr::getUsrp`
- `Sdr::gpsLock`
- `Sdr::refLoLockDetect`
- `Sdr::setRFParams`
- `Sdr::setupGpio`
- `Sdr::setupRx`
- `Sdr::setupTx`

## Doxygen warnings

Comments that Doxygen could read but that do not match the code, for example a `@param` naming an argument the function does not have.

- `sdr/main.cpp:92`: argument 'pulses_received' of command @param is not found in the argument list of checkForFullSampleSum(Chirp &amp;chirp, vector&lt; complex&lt; float &gt; &gt; &amp;sample_sum, ofstream &amp;outfile)
- `sdr/main.cpp:92`: argument 'error_count' of command @param is not found in the argument list of checkForFullSampleSum(Chirp &amp;chirp, vector&lt; complex&lt; float &gt; &gt; &amp;sample_sum, ofstream &amp;outfile)
- `sdr/main.cpp:92`: argument 'last_pulse_num_written' of command @param is not found in the argument list of checkForFullSampleSum(Chirp &amp;chirp, vector&lt; complex&lt; float &gt; &gt; &amp;sample_sum, ofstream &amp;outfile)
- `sdr/main.cpp:125`: argument 'last_pulse_num_written' of command @param is not found in the argument list of splitOutputFiles(Chirp &amp;chirp, ofstream &amp;outfile, string &amp;current_filename, int &amp;save_file_index)
- `sdr/main.cpp:156`: argument 'error_count' of command @param is not found in the argument list of wrapUp(boost::asio::posix::stream_descriptor &amp;gps_stream, ofstream &amp;outfile, string &amp;current_filename, boost::thread_group &amp;transmit_thread)
- `sdr/main.cpp:156`: argument 'last_pulse_num_written' of command @param is not found in the argument list of wrapUp(boost::asio::posix::stream_descriptor &amp;gps_stream, ofstream &amp;outfile, string &amp;current_filename, boost::thread_group &amp;transmit_thread)
- `sdr/main.cpp:156`: argument 'pulses_received' of command @param is not found in the argument list of wrapUp(boost::asio::posix::stream_descriptor &amp;gps_stream, ofstream &amp;outfile, string &amp;current_filename, boost::thread_group &amp;transmit_thread)
