.. Allow bash inline coding. Will only include line numbers if code has 5 of more lines.
.. highlight:: bash
   :linenothreshold: 5 


Getting Started
===============
There are two implementations for this project. One utilizes cloud storage, while the other relies on local storage.

.. tip::
    Before settings up this project, install Python 3.8 or later; support for Python 3.7 and earlier is deprecated for some libraries in this project. 


#############
Project Setup
#############

.. note::

    The below setup is for MAC OS only. I will be providing setup instructions for Windows OS in a later update.

Install `PostgreSQL <https://postgresapp.com/>`_ and start the database server. You can watch the 
`MAC OS installation video <https://youtu.be/qw--VYLpxG4?si=KPDT8niVeJ_GPGOS&t=654>`_ to assist you with the installation.

After installing PostgreSQL, you will need to complete the below steps so that the ``psql`` command will work in Terminal:

    #. Open the PostgreSQL app and make sure the server is runnning by clicking Start. 
    #. Click on Server Settings and copy the Binaries path.
        .. figure:: images/postgresql_binaries_path.png
           :alt: This is an image
    #. Open Terminal, paste ``sudo nano /etc/paths``, and press Enter. 
        .. note::
            
            You will be prompted to enter a password to edit the ``paths`` file.
    #. Paste the Binaries path in the ``paths`` file.
    #. Press ``Control + O``, then Enter to write to the ``paths`` file.
    #. Lastly, press ``Control + X`` to exit the ``paths`` file.

Now, when opening Terminal, you will be able to use the ``psql`` command.

.. caution::

    If you do not complete the above steps, then you will get ``psql: command not found`` when trying to execute the ``psql`` command in Terminal.

To begin this project you will first need to clone the GitHub repository to your desired directory by running the below command in Terminal::

    git clone https://github.com/tyrawls/portfolio-optimization.git

Cloud Storage
-------------

.. note::

    To configure this setup, you'll be required to establish three components within Amazon Web Services (AWS).

    - `Amazon S3 <https://aws.amazon.com/s3/>`_
    - `Amazon Lambda <https://aws.amazon.com/pm/lambda/>`_
    - `Amazon RDS <https://aws.amazon.com/rds/?p=ft&c=db&z=3>`_ (PostgreSQL instance)

Navigate to the cloud storage directory after you have cloned the GitHub repository::

    cd portfolio-optimization/cloud-storage

Create a Python virtual environment and activate it::

    python -m venv .venv              # create the environment
    source .venv/bin/activate         # activate the environment for Mac and Linux

Install the cloud dependencies (requirements) into the Python virtual environment::

    pip install -r requirements.txt


Local Storage 
-------------

Navigate to the local storage directory after you have cloned the GitHub repository::

    cd portfolio-optimization/local-storage

Create a Python virtual environment and activate it::

    python -m venv .venv              # create the environment
    source .venv/bin/activate         # activate the environment for Mac and Linux

Upgrade pip version::

    pip install --upgrade pip

Install the local dependencies (requirements) into the Python virtual environment::

    pip install -r requirements.txt

Install the dbt-postgres adapter version used for this project::

    python -m pip install dbt-postgres==1.7.0













    
