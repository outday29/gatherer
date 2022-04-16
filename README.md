Overview
--------
Gatherer is a command line utility built for Taylor's students to automatically download course materials from TIMeS website into your local machine. 

Installation
------------
First, install [Git](https://git-scm.com/) in your local machine. Then, clone the repository using the following command:

```
git clone https://github.com/Whatever929/gatherer
```
```
cd gatherer
```

Then, install the dependencies located in the `requirements.txt`.

```
pip install -r requirements.txt
```

Usage
-----
To download course material, execute the command

```
python main.py -c
```

Gatherer will request for login information when logging in for the first time. The login information will be stored in file path specified in `config.py`.
The materials will be downloaded into folder specified in `config.py`, which by default is `"D:/School_Material/"`. 
Users can configure the folder location by changing the `config.py` file.

For more information, one can read the help information:
```
python main.py -h
```

Demo
----
https://user-images.githubusercontent.com/60956360/163658812-68f26f02-f0bb-4080-b32a-ec9c1c851977.mp4

Note
----
1. There will be a 3 seconds timeout after downloading each item to prevent overloading the TIMeS servers.

Author
------
Ong Eng Kheng 
- Github: https://github.com/Whatever929/
