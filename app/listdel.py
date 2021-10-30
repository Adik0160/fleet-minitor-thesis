polaczenie = []
polaczenie.append({'wsHandler': 'handler1', 'deviceNr': 1234})
polaczenie.append({'wsHandler': 'handler2', 'deviceNr': 567})
polaczenie.append({'wsHandler': 'handler3', 'deviceNr': 11223})

print(polaczenie)

for i in range(len(polaczenie)):
    if polaczenie[i]['wsHandler'] == 'handler3':
        del polaczenie[i]
        break

print(polaczenie)