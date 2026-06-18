---
title: Open Radar Code Architecture
---

{{< blocks/cover title="Open Source Radar Sounding for Studying the Environment" image_anchor="top" height="full" >}}
<a class="btn btn-lg btn-primary me-3 mb-4" href="docs/">
  Learn More <i class="fas fa-arrow-alt-circle-right ms-2"></i>
</a>
<a class="btn btn-lg btn-primary me-3 mb-4" href="https://ieeexplore.ieee.org/document/10639440">
  Read the Paper <i class="fas fa-book ms-2 "></i>
</a>
<a class="btn btn-lg btn-secondary me-3 mb-4" href="https://github.com/radioglaciology/uhd_radar/">
  Download <i class="fab fa-github ms-2 "></i>
</a>
<p class="lead mt-5">The Open Radar Code Architecture (ORCA) is a community-formed initiative created to make radar-sounding research accessible through open-source code, instruction manuals, and forums, enabling teams to use low-cost Software-Defined Radios (SDRs) as radars. </p>
{{< blocks/link-down color="info" >}}
{{< /blocks/cover >}}


{{% blocks/lead color="primary" %}}
Deploying radar based on software-defined radios typically requires a year or more of development overhead. ORCA aims to streamline radar technology development by minimizing repeated efforts, reducing the barrier to entry, and promoting shared innovation.

By establishing an open-source ecosystem, ORCA lays a foundation for a community that collaborates on tool development and accelerates environmental discovery.

This website provides documentation for the ORCA codebase, along with instructions for building open-source instruments including general <b>software-defined radars</b>, <b>Peregrine</b>, and <b>MAPPERR</b>.

We also provide general strategies for extending our code to develope radar instruments
customized to your research needs. [Check out the full ORCA codebase here](https://github.com/HI-SNR-Lab/uhd_radar).
{{% /blocks/lead %}}


{{% blocks/section color="dark" type="row"%}}

<div style="text-align: center; margin-bottom: 40px; padding-top: 40px;">
  <h2>Open-Source Instruments</h2>
</div>



{{% blocks/feature icon="fa-gears" title="Software-Defined Radar" url="docs/radar" %}}
Our software-defined radar code works with most Ettus USRP software-defined radios.
With a few hardware components and one YAML file, you can build a radar system, customized
for your research needs.
{{% /blocks/feature %}}


{{% blocks/feature title="Peregrine UAS" url="docs/peregrine" icon="fa-plane-departure" %}}
Use our guide to build Peregrine, a field-portable fixed-wing UAV equipped with a miniaturized ice-penetrating radar system.
{{% /blocks/feature %}}


{{% blocks/feature icon="fa-map" title="MAPPERR" url="docs/mapperr" %}}
Use our guide to build MAPPERR, a multi-frequency snowmobile-towed ice-penetrating radar-radiometer system.
{{% /blocks/feature %}}


{{% /blocks/section %}}

{{% blocks/lead %}}


The [HI-SNR Laboratory](https://hisnr.com/) {{< fa "fa-solid fa-envelope" "mailto:hisnr-lab@colorado.edu" >}} at the University of Colorado, Boulder is currently leaading the ORCA initiative. 

ORCA was originally developed by the Stanford [Radio Glaciology Lab](https://www.radioglaciology.com).

<div style="display: flex; justify-content: center; gap: 20px; align-items: center; width: 100%;">
{{< figure src="images/HI-SNR.png" alt="HI-SNR Laboratory Logo" width="150px"  >}} 
{{< figure src="images/RADIO-logo.png" alt="Radio Laboratory Logo" width="150px" >}}
</div>

{{% /blocks/lead %}}