# Insight Coding Challenge
[Details of challenge can be found at - https://github.com/InsightDataScience/coding-challenge]

Author: Prashant Ratnaparkhi
## Solution Overview 
Two Python files in the src directory contain 2 different implementations. First imlementation (payment_median_degree.py) uses 
networkx Python Package to implement Venmo Payment graph. Second implementation (payment_median_degree1.py) contains implementation 
of classes to represent Venmo Payment Graph. Second implementation does not require networkx package, and in this case, PaymentGraph 
consists of list of Pariticipant objects and list of Transaction objects. Each Participant object has name and list of neighbor names. 
Eash Transaction object has payor-name, payee-name and timestamp. Methods required, only to complete the challenge, are implemented for 
the three classes - PaymentGraph, Participant and Transaction. The logic of the main function is same in both implementations and it 
handles addition of edges, vertex counting and median calculations. Updating the graph based on sixty seconds moving window is done 
in the main function. Very basic error handling is imlemented. Raising & handling exceptions, and handling errors need improvements. 

11 test cases are used to test and are in test suite directory. These test basic functionlity and large (20K+) payments among other 
items. Implementation is also tested with test files supplied by Insight. 

## Development Environment
64 bit Windows 2000 with Git Bash, Python 3.4.3 (with netowkx and statistics packages)

## Test Environment 
Unix VM on koding.com with 3.13.0-29-generic #53-Ubuntu and Python 2.7.6  (Used for clean environment testing)  
64 bit Windows 2000 with Git Bash, Python 3.4.3 (with netowkx and statistics packages)

## Commands to install required packages and test
On Widows
* pip install networkx 
* pip install statistics
[It may be necessary to install pip using get-pip.py]

On koding.com vm:
* sudo apt-get update
* sudo apt-get install python-pip
* sudo pip install statistics
* sudo pip install networkx 
* chmod +x ./run_test.sh 
