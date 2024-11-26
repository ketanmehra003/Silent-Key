with open('key_p.bin', 'rb') as f:
    key = f.read()
    print(key, len(key), sep='\n')