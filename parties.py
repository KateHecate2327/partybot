
import datetime
from typing import List


class Party:
    day: datetime.date
    chat_id: str
    participants: List[str]

    def __init__(self, chat_id: str):
        self.day = datetime.date.today()
        self.chat_id = chat_id
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)
    
    def mention(self):
        mention = "Не забудьте позвонить в охране"
        for p in self.participants:
            mention += f", @{p}"
        return mention


class Parties:
    last_party: Party

    def __init__(self):
        self.last_party = None

    def get_party(self):
        # if self.last_party and self.last_party.day == datetime.date.today():
        return self.last_party
        
    def new_party(self, chat_id):
        new_party = Party(chat_id)
        self.last_party = new_party
        return new_party
