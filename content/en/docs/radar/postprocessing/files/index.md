---
title: File Formats
description: How data is stored from the ORCA system
weight: 10
---

# rx_samps.bin
This is the raw data gathered from the receive file. The format of the bin file is <1st real><1st imag><2nd real><2nd imag>. This is I/Q sampling where the I are the real values and the Q is the imaginary values. The real and imaginary parts of the signal are of type float32.

What is I/Q sampling? It stands for in-phase and quadrature sampling. Quadrature means for something to have 90 degree separation which is the phase seperation between a cosine and sine function. The in-phase samples would come from the cosine wave and the quadrature samples come from the sine wave. The combination of sine and cosine waves are able to make up the waves used for radar. The reason for using the information from sine and cosine to plot the received wave is because we can gain information on the phase of the wave. Phase information is good for detecting if an object is moving. 