# Server log analysis
Implementation of basic analytics on server log file:
* identify most popular resources on the site that consume the most bandwidth;
* list in descending order the site’s 10 most frequently visited 60-minute period;
* find active hosts/IP addresses that have accessed the site;
* detect patterns of three consecutive failed login attempts over 20 seconds and log all further attempts to reach the site from the same IP address for the next 5 minutes.

## Prerequisites
[Python 3.6](https://www.python.org/downloads/)

## Installing 
`git clone https://github.com/msurmenok/insight-data-challenge.git`

## Running the tests
In terminal/console
* change current directory to insight_testsuite
`cd insight-data-challenge\insight_testsuite\`
* run run_tests.sh
`./run_tests.sh`

## License
Code released under the [MIT License](https://github.com/msurmenok/insight-data-challenge/blob/master/LICENSE)
