# adjustTask
**Installation**

To run the application you need to create a python virtual environment, here ia a link to a guide for reference:

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

After activating it, simply install all the packages in the requirements.txt file. for example via 
`pip install -r requirements.txt`

then the django app can be started:
`python manage.py runserver`

some enviromental variables have to be set in case of troubles starting the app, for example on MacOS:

`
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=adjustTask.settings
`

this will just run a local server with the application at localhost:8000

**Application**

The main parts of the application are:
    Adjsut.modules.dataset.operations --> it contains all the operations that can be performed on the dataset
    Adjsut.modules.support.response.helper --> it contains the helper functions for the dataset view
    Adjust.models --> it contains the dataset model
    Adjust.views --> it contains the view to serve the dataset operations
    adjustTask.urls --> it contains the urls of the application

    FILTERS
    
    date: format yyyy-mm-dd ex. 2017-06-01
        date_from and date_to, set them both for a time range, set them both equal for a single day, 
        set just date_from for greater than that date, set just date to for lesser than that date
    
    channels, countries, os: list of string, has to be set multiple time in the URL, used for filtering the 3 fields 
        ex. dataset/?countries=CA&countries=US
    
    aggregation_list, group_by: they need to be set together and get a list of string. The aggregation list determines 
        on which column to make the SUM() operation, it can have any of the summable columns plus cpi for returning the 
        cpi aggregation metric.
        The group by indicates for which column to group by, it can be used for multiple non numerical columns
    
    order_by: gets just one string, indicating the column for which to order by
        ex. -col_name --> DESC, col_name -->ASC
    
USE CASES

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order:

    http://127.0.0.1:8000/dataset/?date_to=2017-06-01&aggregation_list=impressions&aggregation_list=clicks&group_by=country&group_by=channel&order_by=-clicks
    
2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order:

    http://127.0.0.1:8000/dataset/?date_from=2017-05-01&date_to=2017-05-31&order_by=date&group_by=date&aggregation_list=installs&os=ios
    
3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order:

    http://127.0.0.1:8000/dataset/?date_from=2017-06-01&date_to=2017-06-01&order_by=-revenue&group_by=os&aggregation_list=revenue
    
4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order:

    http://127.0.0.1:8000/dataset/?order_by=-cpi&group_by=channel&aggregation_list=cpi&aggregation_list=spend&country=CA