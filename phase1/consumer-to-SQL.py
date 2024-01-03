from kafka import KafkaConsumer, TopicPartition
from json import loads
import models
from database import engine, Session

models.Base.metadata.create_all(bind=engine)


class XactionConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer('bank-customer-events',
            bootstrap_servers=['localhost:9092'],
            # auto_offset_reset='earliest',
            value_deserializer=lambda m: loads(m.decode('ascii')))
        # These are two python dictionaries
        # Ledger is the one where all the transaction get posted
        self.ledger = {}
        # custBalances is the one where the current balance of each customer account is kept.
        self.custBalances = {}
        # THE PROBLEM is every time we re-run the Consumer, ALL our customer data gets lost!
        # add a way to connect to your database here.
        self.db = Session()

    def handleMessages(self):
        for message in self.consumer:
            message = message.value
            print('{} received'.format(message))
            self.ledger[message['custid']] = message
            # add message to the transaction table in your SQL using SQLalchemy
            self.addTransaction(message)
            # add or update the customers balance for each transaction
            self.calculateBalance(message)
            if message['custid'] not in self.custBalances:
                self.custBalances[message['custid']] = 0
            if message['type'] == 'dep':
                self.custBalances[message['custid']] += message['amt']
            else:
                self.custBalances[message['custid']] -= message['amt']
            print(self.custBalances)

    # Get the message, create a txn, add and commit it to Transaction table in db
    def addTransaction(self, message):
        txn = models.Transaction(
            custid=message['custid'],
            type=message['type'],
            date=message['date'],
            amt=message['amt']
        )
        self.db.add(txn)
        self.db.commit()

    # Get the message, if customer exists then update their balance, if they don't exist then create a record with balance
    def calculateBalance(self, message):
        db = self.db
        is_cust = db.query(models.Balance).filter(models.Balance.custid == message['custid']).first()
        if is_cust:
            if message['type'] == 'dep':
                is_cust.balance += message['amt']
            else:
                is_cust.balance -= message['amt']
            db.commit()
        else:
            if message['type'] == 'dep':
                customer = models.Balance(
                    custid=message['custid'],
                    balance=message['amt']
                )
            else:
                amount = 0 - message['amt']
                customer = models.Balance(
                    custid=message['custid'],
                    balance=amount
                )
            self.db.add(customer)
            self.db.commit()

if __name__ == "__main__":
    c = XactionConsumer()
    c.handleMessages()
