.. Allow bash inline coding. Will only include line numbers if code has 5 of more lines.
.. highlight:: bash
   :linenothreshold: 50 


Project Setup
=============
There are two implementations for this project. One utilizes cloud storage, while the other relies on local storage.

.. tip::
    Before settings up this project, install Python 3.8 or later; support for Python 3.7 and earlier is deprecated for some libraries in this project. 

.. note::
   This setup is for MAC OS only. I will be providing setup instructions for Windows OS in a later update.

****************
PostgreSQL Setup
****************

Installation
------------
Install `PostgreSQL <https://postgresapp.com/>`_ and start the database server. You can watch the 
`MAC OS installation video <https://youtu.be/qw--VYLpxG4?si=KPDT8niVeJ_GPGOS&t=654>`_ to assist you with the installation.

Configure PATHS File
--------------------
After installing PostgreSQL, you will need to complete the below steps so that the ``psql`` command will work in Terminal. 
These steps will add the PostgreSQL binaries path to the ``paths`` file on your computer:

    #. Open Terminal and type ``sudo nano /etc/paths``, then press Enter to open the ``paths`` file. 
        .. note::
            You will be prompted to enter a password to edit the ``paths`` file.
    #. Open the PostgreSQL app and make sure the server is runnning by clicking Start. 
    #. Click on Server Settings and copy the binaries path.
        .. figure:: images/postgresql_binaries_path.png
           :alt: This is an image
    #. Paste the binaries path in the ``paths`` file in Terminal.
        .. figure:: images/paths_file_content.png
           :alt: This is an image
    #. Press ``Control + O``, then Enter to save the contents to the ``paths`` file.
    #. Lastly, press ``Control + X`` to exit the ``paths`` file.

Upon relaunching Terminal, you should find that you can now utilize the ``psql`` command. 

.. caution::
    If you do not complete the above steps, then you will get ``psql: command not found`` when trying to execute the ``psql`` command in Terminal.

.. note::
    The below setup is for the local implementation only. If you're not using the local setup, please skip to :ref:`Clone GitHub Repo`. 


Set Password
------------
We need to set a password for the local database connection which will be used later to connect ``dbt``.
Enter the below in Terminal to launch the PostgreSQL commandline::

    psql -U postgres

To set the password, enter ``\password postgres``. You'll be prompted to create a password.

Create Database
----------------
You must establish a database called ``company_stock`` to store the stock data. Upon successful creation, 
you should observe it within the PostgreSQL app. 

Enter the below command in the PostgreSQL commandline::

    CREATE DATABASE company_stock;

Enter ``\q`` in the PostgreSQL commandline to exit. Open the PostgreSQL app to verify that the database was created

.. figure:: images/postgresql_company_stock_database.png
    :alt: This is an image

*****************
Clone GitHub Repo 
*****************
Open Terminal and navigate to a directory of your choice. Clone the GitHub repository by running the below command::

    git clone https://github.com/tyrawls/portfolio-optimization.git

This will copy all the project files to your directory.

********************
Install Dependencies
********************
Navigate to the cloud or local storage directory in Terminal after you have cloned the GitHub repository::

    cd portfolio-optimization/cloud-storage      # directory for cloud setup
    cd portfolio-optimization/local-storage      # directory for local setup

.. note::
    You only need to choose one directory. The local directory is more simple, but the cloud directory requires more setup.
    To configure the cloud setup, you'll be required to establish three components within Amazon Web Services (AWS).

    - `Amazon S3 <https://aws.amazon.com/s3/>`_ storage for staging data
    - `Amazon Lambda <https://aws.amazon.com/pm/lambda/>`_ to trigger data transfer to the database
    - `Amazon RDS <https://aws.amazon.com/rds/?p=ft&c=db&z=3>`_ for PostgreSQL database storage

Create a Python virtual environment and activate it::

    python -m venv .venv              # create the environment
    source .venv/bin/activate         # activate the environment for Mac and Linux

Upgrade the pip version::

    pip install --upgrade pip

Install the dependencies (requirements) into the Python virtual environment::

    pip install -r requirements.txt

*********
dbt Setup
*********

Installation
------------
Install the ``dbt-postgres`` adapter version used for this project::

    python -m pip install dbt-postgres==1.7.0

After the installation, check the ``dbt`` version::

    dbt --version

You should see::

    Core:
    - installed: 1.7.0 

    Plugins:
    - postgres: 1.7.0

.. note::
    It may say that there's an update available, but this can be ignored. Just make sure that the ``dbt-core`` 
    version matches the ``dbt-postgres`` version.

Initialization
--------------

Now you will need to create the ``profiles.yml`` file to add your database credentials. 
Open a new Terminal window. Copy and paste the below::

    cd ~                    # switch to root directory
    mkdir .dbt              # create .dbt folder
    cd .dbt                 # switch to .dbt folder
    touch profiles.yml      # create yml file for database connections
    nano profiles.yml       # open yml file for editing
       
Copy and paste the below in the ``profiles.yml`` file::

    portfolio_optimization_project_dbt:
    outputs:
        dev:
        type: postgres
        threads: 1
        host: [host]
        port: 5432
        user: [dev_username]
        pass: [dev_password]
        dbname: company_stock
        schema: public

        prod:
        type: postgres
        threads: 1
        host: [host]
        port: [port]
        user: [prod_username]
        pass: [prod_password]
        dbname: [dbname]
        schema: [prod_schema]

    target: dev 

You will need to modify the inputs listed below:

.. note::
    The brackets will need to be removed for each input and the password would need to be in single quotes.

* **host**: If you are configuring this locally, then assign this value to ``localhost``. If you're using the cloud setup then you will need to enter the AWS RDS endpoint you created.
* **dev_username**: If you are configuring this locally, then assign this value to ``postgres``. If you're using the cloud setup then you will need to enter the AWS RDS username you created.
* **dev_password**: If you are configuring this locally, then assign this value to the password you created in the :ref:`PostgreSQL Setup`. If you're using the cloud setup, then you will need to enter the AWS RDS username you created.


To save the ``profiles.yml`` content:

* Press ``Control + O``, then Enter to write to the ``profiles.yml`` file.
* Lastly, press ``Control + X`` to exit the ``profiles.yml`` file.