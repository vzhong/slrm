import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--city', default='seattle')
parser.add_argument('--state', default='wa')
args = parser.parse_args()


print('{}, {}'.format(args.city, args.state))
