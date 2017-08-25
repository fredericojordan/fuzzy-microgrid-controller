# fuzzy-microgrid-controller

Simple implementation of a fuzzy microgrid controller.

Inputs "power balance" and "battery state of charge" are fuzzified into 5 triangular fuzzy sets each and combined to produce a fuzzy "battery power output", which is then transformed into a crisp value using the centroid point.

Inspired by [this paper](http://ieeexplore.ieee.org/document/7796362/).

## Images

Rule-Based Controller:
![Rule-Based Controller](http://i.imgur.com/D18VOtN.png)

Fuzzy Inference System
![Fuzzy Inference System](http://i.imgur.com/oTkOL9h.png)
