# Seismometer records of ground tilt induced by debris flows

Jupyter notebook containing code and data to reproduce the results shown in Wenner et al., submitted to BSSA

In this project, we use recordings of broadband seismometers to measure ground tilt caused by the passing of a debris flow.
Seismic data of the Volcán de Fuego, Guatemala is not publically available. Addtionally, force plate data of Illgraben is also not publically available.
All other data can be found in the data directory.

*I am still in the process of uploading and adjusting all the code to the clean data structure. I apologize for any inconveniences!*

## Prerequisites

* Create new environement

```
conda create -n tilt 
```

* Activate environment
```
conda activate tilt
```

* Install packages

```
conda install numpy scipy obspy pandas matplotlib
```

```
conda config --add channels conda-forge
```

## File explanation

