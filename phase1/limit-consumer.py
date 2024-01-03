from kafka import KafkaConsumer, TopicPartition
from json import loads

class LimitConsumer:
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
        # balanceLimit is the lowest negative value allowed, any value lower should print a warning.
        self.balanceLimit = -5000


    def handleMessages(self):
        for message in self.consumer:
            message = message.value
            print('{} received'.format(message))
            self.ledger[message['custid']] = message
            if message['custid'] not in self.custBalances:
                self.custBalances[message['custid']] = 0
            if message['type'] == 'dep':
                self.custBalances[message['custid']] += message['amt']
            else:
                self.custBalances[message['custid']] -= message['amt']
            self.determineViolations()
            # Need to figure out which customers are over a certain

    def determineViolations(self):
        violators = [custid for custid, balance in self.custBalances.items() if balance <= self.balanceLimit]
        print(f"Customer who are in violation of minimum balance ( {self.balanceLimit} ): {violators}")

