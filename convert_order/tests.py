import random 

def crypt_id(id):
    id_new_str = str(id)
    letters = 'abcdefghijklmnopqrstuvwxyz'

    NUM_OF_LETTERS = 7
    for _ in range(NUM_OF_LETTERS):
        random_index = random.randint(0, len(str(id_new_str))-1)
        id_new_str = id_new_str[:random_index] + random.choice(letters) + id_new_str[random_index:]
    return id_new_str

word = '14'
print(crypt_id(word))


