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

To begin this project you will first need to clone the GitHub repository to your desired directory by running the below command::

    git clone https://github.com/tyrawls/portfolio-optimization.git

You will then need to complete the steps for the cloud or local storage depending on which setup you want to deploy.

.. tip::
    I would suggest setting up the local storage as the cloud storage requires AWS services as a prerequisite.


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

Navigate to the dbt project folder::

    cd portfolio_optimization_project_dbt

Create a Python virtual environment for the dbt project and activate it::

    python -m venv dbt-env            # create the environment
    source dbt-env/bin/activate       # activate the environment for Mac and Linux 

Install the dbt-postgres adapter::

    python -m pip install dbt-postgres==1.7.0

Install dbt-init::

    pip install dbt dbt-init









    
