from faker import Faker
from string import ascii_letters

def generate_random_string():

    allowed = ascii_letters + '-'
    fake = Faker('it_IT')
    name = fake.name()
    continuous_name = '-'.join(name.split(" "))
    clean_name = "".join()



class CloudManagerOperation:

    def __init__(self):

        pass

    def get_unique_machine_name(self):

        while True:
            pass