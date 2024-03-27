.. Allow bash inline coding. Will only include line numbers if code has 5 of more lines.
.. highlight:: bash
   :linenothreshold: 50 


Deployment
==========
This project was deployed using `Streamlit`. To deploy `Streamlit`, you will need to navigate to the ``local-storage`` or 
``cloud-storage`` folder via Terminal depending on which setup you configured. This folder will contain a file called ``app.py`` 
which will be used to deploy the application.

Execute the below in Terminal to deploy the application::

   streamlit run app.py

You should see an application interface that looks like the below.

