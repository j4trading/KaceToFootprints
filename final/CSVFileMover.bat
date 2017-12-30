REM created 10/06/2017 
REM batch file copies file to footprints server while overwriting
REM also writes to an error log file in case we have trouble also overwriting

REM include date and time
echo %date%, %time% >logerror.txt
echo. >>logerror.txt

REM deleting net use before the fact to prevent being unable to connect to server
net use \\ussighnynt12.us.int.sonichealthcare\imports /delete /y

echo net use yields this error: >>logerror.txt
net use \\ussighnynt12.us.int.sonichealthcare\imports /user:us\sitkace Austin123 2>> logerror.txt

echo.>>logerror.txt
echo copying file yields this error: >>logerror.txt
copy "Footprints Export_Output.csv" "\\ussighnynt12.us.int.sonichealthcare\imports\Footprints Export_Output.csv" 2>> logerror.txt

echo.>>logerror.txt
echo deleting net use yields this error: >>logerror.txt
net use \\ussighnynt12.us.int.sonichealthcare\imports /delete /y 2>>logerror.txt

