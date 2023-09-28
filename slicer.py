import os

path = './img/pieces/'
listName = os.listdir(path)

for old in listName:
    piece = old.replace("s", "")
    new = piece + '.png'
    print(new)
    try:
        os.rename(path + old, path + new)
        print('Successfully renamed')
    except:
        print('Failed to rename')
