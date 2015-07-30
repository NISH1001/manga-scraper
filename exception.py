#!/usr/bin/env python3

class MangaError(Exception):
    def __init__(self, args):
        self.args = args

    def display(self):
        print(''.join(self.args))

def main():
    pass

if __name__=="__main__":
    main()

