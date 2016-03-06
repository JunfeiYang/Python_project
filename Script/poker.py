#!/usr/bin/env python
def poker():
    values = range(1,54)+ 'Jack Queen King'.split()
    suits = 'diamonds clubs hearts spades'.split()
    deck = ['%s of %s'%(v,s) for v in values for s in suits ]
    
    #
    from pprint import pprint
    from random import shuffle
    shuffle(deck)
    pprint(deck[:12])
    while deck:
         raw_input(deck.pop())

if __name__ == '__main__':
         poker()
