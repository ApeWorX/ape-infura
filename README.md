# Quick Start

Use the [Infura](https://infura.io/) provider plugin to interact with blockchains via APIs.
This plugin supports the following ecosystems:

- Ethereum
- Polygon
- Arbitrum
- Optimism
- Blast
- ~~Linea~~ (awaiting ape-linea update)

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
```

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
