import argparse

def get_context():
    parser = argparse.ArgumentParser(description='Uses the graph.json to generate a context for a type.')
    parser.add_argument('graph', type=str, help='The file to use to generate the context network.json')
    args = parser.parse_args()
    return args.context