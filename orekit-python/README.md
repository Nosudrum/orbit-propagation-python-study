# Orekit (python wrapper)

This library was not investigated as part of the May-July 2022 research internship, but the following instructions are
still provided as a quick means to get started with Orekit(py).

## Introduction

[Orekit](https://www.orekit.org/) (ORbit Extrapolation KIT) is a free java library providing basic space dynamics
objects and services. The
[python-wrapper](https://gitlab.orekit.org/orekit-labs/python-wrapper) project allows using orekit in a python
environment.

## Installation

You can install Orekit(py) in a new dedicated environment called *orekitpy* by navigating to this directory and running
the following command :

```
conda env create -f orekitpy.yaml
```

## Orekit data

For Orekit to work, the ['orekit-data.zip'](orekit-data.zip) file must be present in this directory. If it is not, or to
update it, you can download it from its [dedicated repository](https://gitlab.orekit.org/orekit/orekit-data) and rename
it from `orekit-data-master.zip` to `orekit-data.zip`.

## PyCharm specificity

The PyCharm IDE, developed by JetBrains, performs variable inspections in a way that is not compatible with the orekit
wrapper. As such, displaying variable values automatically or on demand from the variables list will result in an error
and the shutdown of the Java VM.

To circumvent this issue, install ipython in your environment with `conda activate orekitpy`
and `conda install ipython`, and make sure that PyCharm is configured to use it for the python console.
The **variables loading policy** must also be set to **on demand**.

Variables can then successfully be called in the python console without resulting in a crash of the JVM.



