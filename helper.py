import random
import string

class RandomUserData:

    def random_string(self, length):
        special_symbols = "_.-"
        string_symbols = string.ascii_lowercase + string.digits + special_symbols
        random_string = ''
        for i in range(length):
            random_string += random.choice(string_symbols)
        return random_string

    def user_data_generation(self):
        user_data = {}
        user_data['name'] = self.random_string(12)
        user_data['email'] = self.random_string(6) + '@gmail.com'
        user_data['password'] = self.random_string(6)

        return user_data