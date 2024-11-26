# Quick Start

Use the [Metamask Developer](https://developer.metamask.io/) (F.K.A. Infura) provider plugin to interact with blockchains via APIs.
This plugin supports the following ecosystems:

- Arbitrum
- Avalanche
- Base
- Blast
- BSC
- Celo
- Ethereum
- Linea
- Mantle
- Optimism
- Palm
- Polygon
- Scroll
- Starknet
- Unichain
- zkSync

## Dependencies

- [python3](https://www.python.org/downloads) version 3.9 up to 3.12.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-infura
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-infura.git
cd ape-infura
python3 setup.py install
```

## Quick Usage

First, make sure you have one of the following environment variables set (it doesn't matter which one):

- WEB3_INFURA_PROJECT_ID
- WEB3_INFURA_API_KEY

Either in your current terminal session or in your root RC file (e.g. `.bashrc`), add the following:

```bash
export WEB3_INFURA_PROJECT_ID=MY_API_TOKEN

# Multple tokens
export WEB3_INFURA_PROJECT_ID=MY_API_TOKEN1, MY_API_TOKEN2
```

Additionally, if your app requires an API secret as well, use either of the following environment variables:

- WEB3_INFURA_PROJECT_ID
- WEB3_INFURA_API_KEY

And each request will use the secret as a form of authentication.

To use the Infura provider plugin in most commands, set it via the `--network` option:

```bash
ape console --network ethereum:sepolia:infura
```

To connect to Infura from a Python script, use the `networks` top-level manager:

```python
from ape import networks

with networks.parse_network_choice("ethereum:mainnet:infura") as provider:
    # Also, access the websocket URI:
    print(provider.ws_uri)
```
