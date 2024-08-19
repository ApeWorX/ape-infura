import os
import random
from functools import cached_property
from typing import Optional

from ape.api import UpstreamProvider
from ape.exceptions import ContractLogicError, ProviderError, VirtualMachineError
from ape_ethereum.provider import Web3Provider
from web3 import HTTPProvider, Web3
from web3.exceptions import ContractLogicError as Web3ContractLogicError
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware import geth_poa_middleware

_ENVIRONMENT_VARIABLE_NAMES = ("WEB3_INFURA_PROJECT_ID", "WEB3_INFURA_API_KEY")
# NOTE: https://docs.infura.io/learn/websockets#supported-networks
_WEBSOCKET_CAPABLE_ECOSYSTEMS = {
    "ethereum",
    "arbitrum",
    "optimism",
    "polygon",
    "linea",
}


class InfuraProviderError(ProviderError):
    """
    An error raised by the Infura provider plugin.
    """


class MissingProjectKeyError(InfuraProviderError):
    def __init__(self):
        env_var_str = ", ".join([f"${n}" for n in _ENVIRONMENT_VARIABLE_NAMES])
        super().__init__(f"Must set one of {env_var_str}")


class Infura(Web3Provider, UpstreamProvider):
    network_uris: dict[tuple[str, str], str] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __get_random_api_key(self) -> str:
        """
        Get a random api key a private method.
        """
        if keys := self._api_keys:
            return random.choice(list(keys))

        raise MissingProjectKeyError()

    @cached_property
    def _api_keys(self) -> set[str]:
        api_keys = set()
        for env_var_name in _ENVIRONMENT_VARIABLE_NAMES:
            if env_var := os.environ.get(env_var_name):
                api_keys.update(set(key.strip() for key in env_var.split(",")))

        if not api_keys:
            raise MissingProjectKeyError()

        return api_keys

    @property
    def uri(self) -> str:
        ecosystem_name = self.network.ecosystem.name
        network_name = self.network.name
        if (ecosystem_name, network_name) in self.network_uris:
            return self.network_uris[(ecosystem_name, network_name)]

        key = self.__get_random_api_key()

        prefix = f"{ecosystem_name}-" if ecosystem_name != "ethereum" else ""
        network_uri = f"https://{prefix}{network_name}.infura.io/v3/{key}"
        self.network_uris[(ecosystem_name, network_name)] = network_uri
        return network_uri

    @property
    def http_uri(self) -> str:
        # NOTE: Overriding `Web3Provider.http_uri` implementation
        return self.uri

    @property
    def ws_uri(self) -> Optional[str]:
        # NOTE: Overriding `Web3Provider.ws_uri` implementation
        if self.network.ecosystem.name not in _WEBSOCKET_CAPABLE_ECOSYSTEMS:
            return None

        # Remove `http` in default URI w/ `ws`, also infura adds `/ws` to URI
        return "ws" + self.uri[4:].replace("v3", "ws/v3")

    @property
    def connection_str(self) -> str:
        return self.uri

    def connect(self):
        self._web3 = Web3(HTTPProvider(self.uri))

        # Any chain that *began* as PoA needs the middleware for pre-merge blocks
        optimism = (10, 420)
        polygon = (137, 80001, 80002)
        linea = (59144, 59140)
        blast = (11155111, 168587773)

        if self._web3.eth.chain_id in (*optimism, *polygon, *linea, *blast):
            self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self._web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

    def disconnect(self):
        """
        Disconnect the connected API.
        Refresh the API keys from environment variable.
        Make the self.network_uris empty otherwise the old network_uri will be returned.
        """
        self._web3 = None
        (self.__dict__ or {}).pop("_api_keys", None)
        self.network_uris = {}

    def get_virtual_machine_error(self, exception: Exception, **kwargs) -> VirtualMachineError:
        txn = kwargs.get("txn")
        if not hasattr(exception, "args") or not len(exception.args):
            return VirtualMachineError(base_err=exception, txn=txn)

        args = exception.args
        message = args[0]
        if (
            not isinstance(exception, Web3ContractLogicError)
            and isinstance(message, dict)
            and "message" in message
        ):
            # Is some other VM error, like gas related
            return VirtualMachineError(message["message"], txn=txn)

        elif not isinstance(message, str):
            return VirtualMachineError(base_err=exception, txn=txn)

        # If get here, we have detected a contract logic related revert.
        message_prefix = "execution reverted"
        if message.startswith(message_prefix):
            message = message.replace(message_prefix, "")

            if ":" in message:
                # Was given a revert message
                message = message.split(":")[-1].strip()
                return ContractLogicError(revert_message=message, txn=txn)
            else:
                # No revert message
                return ContractLogicError(txn=txn)

        return VirtualMachineError(message, txn=txn)
