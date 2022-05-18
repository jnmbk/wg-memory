# Game of Memory

A board is full of overturned cards. There is a pair for each card. The player flips over two cards. If they match, then they stay overturned. Otherwise they flip back. The player needs to overturn all the cards in the fewest moves to win.

This is one of my weekend game projects where I try to create a simple game in a single weekend.

## Game flow

```mermaid
flowchart TB
s([Start]) --> gc[generate cards]
gc --> m[/card/]
hf{{"len(hand) == 2"}}
m --> hf
hf -- True --> hft[unflip all in hand] --> hft2[remove all in hand] --> sc
hf -- False --> sc
ec{{exact card in hand}} -- True --> ufc["unflip(card)"] --> uh
ec -- False --> ua[disable all cards in hand]
u["unflip all in hand"]
goc{{all cards in game are disabled}} -- True --> e([End])
goc -- False --> uh
ua --> goc
sc{{same card in hand}} -- True --> ec
u --> uh
uh[remove all in hand] --> m
sc -- False --> c2{{"len(hand) < 2"}}
c2 -- True --> a[add card to hand] --> fc[flip card] --> m
c2 -- False --> m
```

# Using

## Setting Up
    git clone git@github.com:jnmbk/wg-memory.git
    cd wg-memory
    pip install -e .

## Running
    python -m game.main

![Tests](https://github.com/jnmbk/wg-memory/actions/workflows/tests.yml/badge.svg)
