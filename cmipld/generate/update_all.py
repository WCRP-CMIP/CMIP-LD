#!/bin/python3

import glob, os, tqdm


def main():
    
    os.system('update_ctx')

    os.system('validjsonld')


    for i in tqdm.tqdm(glob.glob('data_descriptors/*/')):

        os.system('ld2graph '+i)

