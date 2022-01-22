import json
import datetime
import solana
from solana.rpc.api import Client

from random import shuffle



class Airdrop(object):
    def __init__(self, participants):
        if type(participants) == list:
            self.participants = list(set(participants))
        else:
            self.participants = list(set(self.load_participants_from_file(participants)))
        self.accepted_participants = list()
        self.winners = list()
        endpoints = {
            'devnet':'https://api.devnet.solana.com',
            'mainnet':'https://solana-mainnet.phantom.tech'
        }
        self.solana_client = Client(endpoints['mainnet'])

    def logger(self, filename, log_string):
        with open(f'./logs/{filename}.txt', 'a') as f:
            f.write(log_string + "\n")

    def load_participants_from_file(self, path):
        with open(path, 'r') as f:
            return f.read().splitlines()

    def get_wallet_balance(self, wallet):
        return self.solana_client.get_balance(wallet)['result']['value'] / 1000000000

    def exclude_by_balance(self, balance_limit):
        self.logger('balance_check', f'Start time: {datetime.datetime.now()}')
        self.logger('accepted_participants', f'Start time: {datetime.datetime.now()}')
        for participant in self.participants:
            participant_balance = self.get_wallet_balance(participant)
            self.logger('balance_check', f'{participant}|{participant_balance}')
            if participant_balance >= balance_limit:
                self.accepted_participants.append(participant)
                self.logger('accepted_participants', participant)

    def select_random_winners(self, winners_number):
        shuffle(self.accepted_participants)
        self.logger('accepted_participants_shuffled', f'Start time: {datetime.datetime.now()}')
        for participant in self.accepted_participants:
            self.logger('accepted_participants_shuffled', participant)
        self.winners.extend(self.accepted_participants[0:winners_number])
        self.logger('winners', f'Start time: {datetime.datetime.now()}')
        for participant in self.winners:
            self.logger('winners', participant)

        


    def start(self):
        #print(self.get_wallet_balance('C4qZWc7spX7f5Mz925KwYtpCCaFW9j1ieNgXrQLTRDsi'))
        self.exclude_by_balance(0.5)
        self.select_random_winners(3)


if __name__ == "__main__":
    bot = Airdrop('./participants.txt')
    bot.start()