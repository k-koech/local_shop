# NEIGHBORS APPLICATION 
#### The app is a LocalShop App, 20/10/2021
#### **By Kelvin Kipchumba**
## Project Description
    The application allows user to know what is happening in his/her neighborhood most of the time. Its also a platform where important meeting, theft or even death cases are announced
## Setup/Installation Requirements
    - Download a file in the code section to the desired folder
    - Extract the files
    - Open the folder with vs code.
    - Activate the virtual environment in the terminal.
    - Run  ". .env" to source environmet variables and then run "make server" in the terminal.
    - Create database and add its URI in settings.py file.
    - Run migrations using 'python3 manage.py makemigrations' the migrate with 'python3 manage.py migrate'.
    - Open the server http://127.0.0.1:8000/ And you are all done.


## BDD
    A dashboard where clerks can record details for the received items in the store:
    - The number of items received
    - The status of payment(paid or not paid), this is important for procurement processes.
    - The number of items in stock.
    - The number of items spoilt( Broken, expired and anything else).
    - Buying and selling price.
    - On the same dashboard there should be an option to request for more product supply - this request goes to the store admin

    The store admin should be able:
    - To see a detailed report on the performance of individual entries.
    - To approve or decline supply requests from the clerk.
    - To see the products that suppliers have been paid and those not yet - this should be well separated to ensure ease of viewing.
    - To change the payment status to paid for the products that were not paid - Ideally this happens after the suppliers have been paid.
    - To inactivate or delete a clerks account and as well add new clerks.
    - As above mentioned the report should be in a good graphical representation; that is, linear graphs and bar graphs as a requirement - pie charts are totally optional.
    
    The merchant should be able to:
    - Add an admin, deactivate and delete their accounts - PS deactivation is independent from deleting the account, it is important for probation purposes.
    - Should be able to see a store by store report in well visualized graphs
    - To see an individual store performance, even narrowing down to individual product performance.
    - To see the paid and non paid products for each store.

  
## Live link
Deployed project can be accessed here [neighborhood](https://django-neighborhood.herokuapp.com/)   

## Known Bugs
    The application works perfectly well, no bugs.

## Technologies used
    - HTML
    - CSS
    - Javasript
    - Jquery
    - Fontawesome
    - Bootstrap
    - Python

## Support and contact details
    - email :: koechkelvin97@gmail.com
    - phone :: +254725801772

### License
*Licenced under the [MIT-licence](https://github.com/k-koech/localshop/blob/master/LICENSE.md)*
Copyright (c) 2021 **Kelvin Kipchumba, Nicholas Omondi, Franklin Kuloba, Isaiah Morara**
