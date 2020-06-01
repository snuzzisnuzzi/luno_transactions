import requests
import time
import json

secret_key = 'DADw2gjYH_dl9Kg6mLIMck8dqTSdfugJs9PYqYOdTXU'
key_id = 'k3ane3gbrr2pb'

database = []


def read_database():
    """insert a code here to read the data base and get all pending transaction"""

    """if there are values in the database, proceed wto the next line. else, exit function and return to loop"""

    if len(database) > 0:
        file_update = open('transactions.json', 'w')
        json.dump(database, file_update)
        file_update.close()
        make_transfer()


def make_transfer():
    """the next code opens the file and read the transactions"""
    file = open('transactions', 'r')
    lst = json.load(file)
    file.close()
    try:
        """next code calculates the total of all amount to be sent"""
        total = 0
        for t in lst:
            t += float(t[0])
        """next line checks the balance of luno"""
        payload = {'asset': 'XBT'}
        r = requests.get('https://api.mybitx.com/api/1/balance', params=payload)
        rs = requests.get(r.url, auth=(key_id, secret_key)).json()
        luno_balance = rs['balance'][0]['balance']

        """if balance of luno is less than total amount to be sent, send a request t coinbase. else, proceed"""
        if luno_balance < total:
            r = requests.get('https://api.mybitx.com/api/1/funding_address', params=payload)
            rs = requests.get(r.url, auth=(key_id, secret_key)).json()
            luno_address = rs['address']

            #you will insert a code to call the @api view function for sending to coinbase here#

            """next code enters a loop and checks the luno balance in intervals of 15minutes to know when it has been 
            credited"""
            while luno_balance < total:
                time.sleep(900)
                rs = requests.get(r.url, auth=(key_id, secret_key)).json()
                luno_balance = rs['balance'][0]['balance']

        else:
            pass

        """next code sends money to each address in the list serially"""
        for tx in lst:
            payload = {'amount': tx[0], 'currency': 'XBT', 'address': tx[1],
                       'description': tx[2]}
            r = requests.get('https://api.mybitx.com/api/1/send', params=payload)
            print('sending request to luno...')
            rs = requests.post(r.url, auth=(key_id, secret_key)).json()
            print(rs)
            file = open('transactions', 'r')
            lst = json.load(file)
            file.close()

            lst.remove(tx)

            file_update = open('transactions.json', 'w')
            json.dump(lst, file_update)
            file_update.close()

    except Exception as e:
        print(e)
        make_transfer()


"""the following line waits at an interval of 30minutes before carring out the next round of transactions
the reason of the delay is to wait for many addresses to be stored in data base before reading it and carrying out the
next round"""
while True:
    time.sleep(1800)
    read_database()
