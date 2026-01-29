---
title: Open Radar Code Architecture
---

{{< blocks/cover title="Open-source ice-penetrating radar for the cryosphere" image_anchor="top" height="full" >}}
<a class="btn btn-lg btn-primary me-3 mb-4" href="docs/">
  Learn More <i class="fas fa-arrow-alt-circle-right ms-2"></i>
</a>
<a class="btn btn-lg btn-primary me-3 mb-4" href="https://ieeexplore.ieee.org/document/10639440">
  Read the Paper <i class="fas fa-book ms-2 "></i>
</a>
<a class="btn btn-lg btn-secondary me-3 mb-4" href="https://github.com/radioglaciology/uhd_radar/">
  Download <i class="fab fa-github ms-2 "></i>
</a>
<p class="lead mt-5">Open Radar Code Architecture (ORCA) is an open platform for building radar instruments to better understand Earth's coolest places</p>
{{< blocks/link-down color="info" >}}
{{< /blocks/cover >}}


{{% blocks/lead color="primary" %}}
ORCA is a platform for building low-cost, flexible,
and field-proven radar instruments for the cryosphere. ORCA is
the base project for Peregrine, a field-portable ice-penetrating radar UAV,
MAPPERR, a multi-frequency radar/radiometer, and EYAS, a bistatic ice-penetrating radar receiver.

This website provides documentation for the ORCA codebase, along with instructions for building each of these open-source
instruments.

We also provide general strategies for extending our code to develope radar instruments
customized to your research needs.
{{% /blocks/lead %}}


{{% blocks/section color="dark" type="row" %}}
{{% blocks/feature icon="fa-gears" title="Software-defined radar code documentation" url="docs/radar" %}}
Our software-defined radar code works with most Ettus USRP software-defined radios.
With a few hardware components and one YAML file, you can build an
ice-penetrating radar system, customized for your research needs.
{{% /blocks/feature %}}


{{% blocks/feature title="Peregrine UAS" url="docs/peregrine" icon="fa-plane-departure" %}}
Use our guide to build Peregrine, a field-portable fixed-wing UAV equipped with a miniaturized ice-penetrating radar system.
{{% /blocks/feature %}}


{{% blocks/feature icon="fa-map" title="MAPPERR" url="docs/mapperr" %}}
Use our guide to build MAPPERR, a multi-frequency snowmobile-towed ice-penetrating radar-radiometer system.
{{% /blocks/feature %}}


{{% /blocks/section %}}

{{% blocks/lead %}}
ORCA is currently being developed by the University of Colorado Boulder in the Hi-SNR Laboratory. Find their website [here](https://hi-snr-lab.github.io/HI-SNR.github.io/)

ORCA was originally developed by the Stanford Radio Glaciology Lab, whose cool work can be found [here](https://www.radioglaciology.com)! 
{{% /blocks/lead %}}