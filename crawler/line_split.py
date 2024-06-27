from kiwipiepy import Kiwi
kiwi = Kiwi()

with open('./output/namu_data.txt', 'r', encoding='utf-8') as f:
    kiwi_dict = f.read()

result = kiwi.split_into_sents(kiwi_dict)

with open('./output/kiwi_data.txt', 'w', encoding='utf-8') as f:
    for line in result:
        f.write(line.text + '\n')