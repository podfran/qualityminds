# Quickstart
To run the project you will need to setup selenium and pytest. The project requires the firefox and chrome
webdriver to be available from the PATH variable. 

Run your virtualenv, install the dependencies with `pip install -r requirements.txt` and you're good to go.

Run the tests with `pytest`. To run tests in parallel, add the `-n N` option, where `N` is the number of parallel 
processes to be run.

## Reports
To generate test run reports, you will need to run the tests with the `--alluredir=<dir-path>` option, 
where `<dir-path>` is the path (absolute/relative) where the allure files are generated. Then 
[install](https://docs.qameta.io/allure/#_installing_a_commandline) the allure framework (you will need 
[Java](https://java.com/download/) for the cli to work). Then you can run `allure serve <dir-path>` and 
the report will display in a browser window.