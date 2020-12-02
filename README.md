# MAP554 - Multidisciplinary optimization

## Install :

## Setting up the environment
```shell
conda create --name MDO python=3.8
```
### Activating / deactivating the environment :
```shell
conda activate MDO
conda deactivate
```
### Using jupyter lab
```shell
conda install -c conda-forge jupyterlab
```

### Labs

Following is a list of all packages appearing during the labs exercices in the order they appeared. 
With this list installed, you should not need any ```!pip install [package name]``` appearing in the notebook.

#### Lab 1 
```shell
conda install -c conda-forge matplotlib
conda install -c anaconda scipy
conda install -c conda-forge autograd 
conda install numpy
```
#### Lab 2
```shell
conda install -c conda-forge inspyred  
```
#### Lab 3:
[Platypus project on git](https://github.com/Project-Platypus/Platypus)

**Installation**
```shell
conda config --add channels conda-forge
conda install platypus-opt
```
#### Lab 5
Please note that for lab 5, *FELIN* is required and can be found [here](https://github.com/M2CI-ONERA/FELIN.git).
And install this way in *python* - be careful that it will create a new git repository in your current repository (it's not necessarily what you want to do, if you are already in a git repository) : 
```python
!git clone https://github.com/M2CI-ONERA/FELIN.git
```
or in a shell :
```shell
git clone https://github.com/M2CI-ONERA/FELIN.git
```
Other packages :
```shell
conda install -c conda-forge cma 
conda install -c conda-forge openmdao==2.9.1
conda install pandas
conda install -c conda-forge geopy 
```

#### Lab 6 & 7
```shell
conda install scikit-learn
conda install -c conda-forge pydoe2 
```

#### Lab 8 & 9 & 10
```shell
conda install -c conda-forge gpy 
```


