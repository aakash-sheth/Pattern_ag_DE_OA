Data pipeline to process Pattern AG Files

1. You need to keep all your files i.e, crop.csv, weather.csv, spartials.csv, and soil.csv inside one folder (e.g. input folder)
2. Create virtual environment with python with atleast python 3.8 installed.
3. Activate your virtual environment and install all the depencies with 
    > pip install -r requirements.txt
4. To start data pipeline you need to naviate to script folder and run following command
    > python data_pipeline.py
5. Script will ask following to inputs.
    > input folder path
    > output folder path
6. You will find all the processed output files inside provided output folder.
