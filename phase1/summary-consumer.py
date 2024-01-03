from kafka import KafkaConsumer, TopicPartition
from json import loads

class SummaryConsumer:
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
        # need to produce summary stats:  mean deposits, mean withdrawals across all customers
        self.deposits = 0
        self.withdrawals = 0
        self.depositsAmount = 0
        self.withdrawalsAmount = 0


    def handleMessages(self):
        for message in self.consumer:
            message = message.value
            print('{} received'.format(message))
            if message['type'] == 'dep':
                self.deposits += 1
                self.depositsAmount += message['amt']
            else:
                self.withdrawals += 1
                self.withdrawalsAmount += message['amt']
            self.determineStats()

    def determineStats(self):
        if self.deposits > 0:
            dep_mean = self.depositsAmount / self.deposits
        else:
            dep_mean = 0

        if self.withdrawals > 0:
            wth_mean = self.withdrawalsAmount / self.withdrawals
        else:
            wth_mean = 0

        print(f"Deposit Mean: {dep_mean}, Withdrawal Mean: {wth_mean}")

