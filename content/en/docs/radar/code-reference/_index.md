---
title: Code Reference
linkTitle: Code Reference (API)
description: Every class, function and file of the ORCA code, generated from the code with Doxygen
weight: 60
---

The code reference lists every class, function and file in
[uhd_radar](https://github.com/HI-SNR-Lab/uhd_radar): what each one does (when the code has a
comment saying so), its arguments, and a link to its source code. It is built by
[Doxygen](https://www.doxygen.nl) from the code itself, so it shows the code as it was at one
commit. That commit is printed at the top of every page of the reference.

{{% pageinfo %}}
**[Open the code reference](/api/index.html)**
{{% /pageinfo %}}

## Where to start

| To understand... | Open |
|---|---|
| how a whole run is put together | [`run.py`](/api/run_8py.html) and its [`RadarProcessRunner`](/api/classrun_1_1RadarProcessRunner.html) class |
| how the chirp is generated before a run | [`generate_chirp.py`](/api/namespacegenerate__chirp.html) |
| the program that talks to the radio | [`main.cpp`](/api/main_8cpp.html), with the [`Sdr`](/api/classSdr.html) and [`Chirp`](/api/classChirp.html) classes |
| how recorded data is loaded and processed | [`processing.py`](/api/namespaceprocessing.html) and [`processing_dask.py`](/api/namespaceprocessing__dask.html) |

Inside the reference, **Classes** lists the C++ classes, **Namespaces** lists the Python modules,
and **Files** lets you browse folder by folder.

## Writing comments that show up

Doxygen only reads comments written in its own format, so an ordinary `//` or `#` comment above a
function is skipped. The format the project uses is described under "Doxygen Requirements" in the
[uhd_radar style guide](https://github.com/HI-SNR-Lab/uhd_radar/blob/main/STYLEGUIDE.md).
The short version:

```cpp
/**
 * @brief One sentence saying what the function does.
 *
 * @param num_samples Number of samples in the buffer
 * @return true if the buffer was written to the file
 */
bool writeBuffer(size_t num_samples);
```

```python
def load_config(prefix):
    """
    One sentence saying what the function does.

    @param prefix Path of the recording, without its file ending
    @return The configuration as a dictionary
    """
```

[Documentation coverage](coverage/) lists the functions that do not have a description yet.

## Updating the reference

The reference does not update by itself. After the code in `uhd_radar` changes, run this from the
`orca-documentation` folder and commit what it changes:

```bash
python3 doxygen/generate_api_docs.py
```

It needs Python 3, git and [Doxygen](https://www.doxygen.nl/download.html). It downloads the `main`
branch of `uhd_radar`, runs Doxygen, replaces everything in `static/api/` and rewrites the
coverage page. To check your own comments before you push them, point it at your copy of the code:

```bash
python3 doxygen/generate_api_docs.py --source ../uhd_radar
```
