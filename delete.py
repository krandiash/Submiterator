import argparse
from datetime import datetime

from supersubmiterator import mturk_client

parser = argparse.ArgumentParser(description='Interface with MTurk.')
parser.add_argument("--live", action="store_true", default=False)
args = parser.parse_args()

# Get the MTurk client
mturk = mturk_client(args.live)

# Delete HITs
for item in mturk.list_hits()['HITs']:
    hit_id = item['HITId']
    print('HITId:', hit_id)

    # Get HIT status
    status = mturk.get_hit(HITId=hit_id)['HIT']['HITStatus']
    print('HITStatus:', status)

    delete = input('Delete HIT (y/n): ')

    if delete == 'y':
        # If HIT is active then set it to expire immediately
        if status == 'Assignable':
            response = mturk.update_expiration_for_hit(
                HITId=hit_id,
                ExpireAt=datetime(2015, 1, 1)
            )

        # Delete the HIT
        try:
            mturk.delete_hit(HITId=hit_id)
        except:
            print('Not deleted')
        else:
            print('Deleted')
