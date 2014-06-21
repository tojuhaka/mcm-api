mkm-parser
==========

Search for a card from MagicCardMarket with given configuration.

Usage
-----
python mkm.py -c 'Underground Sea' -e 'revised'
python mkm.py -c 'tarmOGoyf' -e 'FutuRe sight' -m -r 2


Configuration:
--------------

add ~/.mkm.cfg:

[MKM]
user = user
domain = https://www.mkmapi.eu/ws
apikey = mkm apikey
condition = EX
reputation = 2
multi = false
