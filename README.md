# Aba Blockchain Commander

Aba Blockchain Commander can be used to control an Aba blockchain node by conversing with a local (or remote) LLM with functional calling

It is licensed under the Apache 2.0 license

This is a minimal implementation used to initiate the Aba blockchain via conversation.

This is not a supported product, but you can ask basic questions in our Aba Project Discord. Thanks for exploring this.

## Install and Configure

REQUIREMENTS: Doesn't support Windows yet; Tested most on Ubuntu

First, install and configure OpenFunctions

https://github.com/ShishirPatil/gorilla/tree/main/openfunctions

LM studio is a great option for running a local LLM server; make sure to start the server

https://lmstudio.ai/

Then install this repository

```
python3 -m venv venv

. ./venv/bin/activate

pip install -r requirements.txt

```

Edit .env file to indicate the directory of your aba-blockchain main install directory, from which you would normally run ". ./activate"

## To Run it

```
. ./venv/bin/activate

python3 abacommander.py
```

and then converse with it by typing out sentences or questions in English

## Use with other chains

You can use with other chains that use the same command structure by changing the value of chain in the abacommander.py file to the cli command for the other chain, e.g. "chia"

## Future Enhancements

This repository can be forked and expanded. Some areas for expansion could include:

- querying the aba node for permitted command line queries

- require user confirmation before submitting any transaction! if you add transactional capabilities

- permit use of an environmental variable to set for a chain other than aba; suggest hardcoding list of chains supported to limit security risk

- potentially connecting to a different functional calling LLM in future

- Add Windows support

- Test w/ MacOS

- Add fingerprint support to wallet show
