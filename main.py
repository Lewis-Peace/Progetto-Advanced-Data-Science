from dataParser import data_parser
from datadownloader import data_downloader

downloader = data_downloader('raw_data')
# text json csv for different types of outputs
parser = data_parser('data', 'csv', 'raw_data')

starting_id, batch = 0, 1000
delete_old_data = True
total_entries = 0

for i in range(starting_id, 360000, batch):
    print(f'Processing data from {i} to {i + batch}')
    downloader.main(i, batch)
    total_entries += parser.main(delete_old_data)
    delete_old_data = False
    #if i + batch % batch * 50 == 0:
    #    print(f'Currently downloaded {total_entries}')
    #    print('Stop downloading? Y/n')
    #    keepComputation = input()
    #    if keepComputation.lower() == 'y':
    #        break
print(f'Loaded {total_entries} boardgames')