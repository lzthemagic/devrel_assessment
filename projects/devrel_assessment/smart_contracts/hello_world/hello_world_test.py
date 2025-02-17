import pytest
import os
from algokit_utils import (
    Account,
    TransactionParameters,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.encoding import decode_address
from algosdk.transaction import PaymentTxn

from smart_contracts.artifacts.hello_world.hello_world_client import HelloWorldClient


@pytest.fixture(scope="session")
def algod_client() -> AlgodClient:
    ALGOD_ADDRESS = os.getenv("ALGOD_SERVER", "http://localhost:4001")
    ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)


@pytest.fixture(scope="session")
def indexer_client() -> IndexerClient:
    INDEXER_ADDRESS = os.getenv("INDEXER_SERVER", "http://localhost:8980")
    INDEXER_TOKEN = os.getenv("INDEXER_TOKEN", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    return IndexerClient(INDEXER_TOKEN, INDEXER_ADDRESS)


@pytest.fixture(scope="session")
def hello_world_client(algod_client: AlgodClient, indexer_client: IndexerClient) -> HelloWorldClient:
    """
    Deploys the HelloWorld contract using a local sandbox account,
    then ensures the contract address is funded for box usage.
    """
    account = get_localnet_default_account(algod_client)
    
    client = HelloWorldClient(
        algod_client=algod_client,
        creator=account,
        indexer_client=indexer_client,
        sender=account.address,
    )

    client.deploy(on_schema_break="append", on_update="append")

    ensure_minimum_balance(algod_client, account, client.app_address, 200_000)

    return client


@pytest.fixture
def p_box_transaction_parameters(hello_world_client: HelloWorldClient) -> TransactionParameters:
    """
    Returns TransactionParameters that reference the 'p'-prefixed box
    used by the contract, based on the current sender address.
    """
    box_prefix = b"p"
    sender_bytes = decode_address(hello_world_client.app_client.sender)
    full_key = box_prefix + sender_bytes
    
    return TransactionParameters(
        boxes=[[hello_world_client.app_id, full_key]]
    )


class TestHelloWorld:
    """
    Test suite for the HelloWorld contract's behavior.
    """

    @pytest.mark.parametrize(
        "name,expected_greeting",
        [
            ("Alice", "Hello, Alice"),
            ("Bob", "Hello, Bob"),
            ("世界", "Hello, 世界"),
        ],
    )
    def test_hello_with_different_names(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
        name: str,
        expected_greeting: str,
    ) -> None:
        """
        Checks if calling 'hello' with valid names returns the correct greeting.
        """
        response = hello_world_client.hello(
            name=name,
            transaction_parameters=p_box_transaction_parameters,
        )
        assert response.return_value == expected_greeting

    def test_hello_empty_name_raises_error(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
    ) -> None:
        """
        Verifies that the contract rejects an empty name, raising an exception.
        """
        with pytest.raises(Exception) as excinfo:
            hello_world_client.hello(
                name="",
                transaction_parameters=p_box_transaction_parameters,
            )

        assert "Name must not be empty" in str(excinfo.value)

    def test_hello_preserves_state(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
    ) -> None:
        """
        Ensures that multiple calls with different names each return the proper greeting 
        (i.e., no unintended overwriting or concurrency issues).
        """
        first_name = "Alice"
        second_name = "Bob"

        first_response = hello_world_client.hello(
            name=first_name,
            transaction_parameters=p_box_transaction_parameters,
        )
        second_response = hello_world_client.hello(
            name=second_name,
            transaction_parameters=p_box_transaction_parameters,
        )

        assert first_response.return_value == f"Hello, {first_name}"
        assert second_response.return_value == f"Hello, {second_name}"

    def test_hello_with_special_characters(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
    ) -> None:
        """
        Confirms the contract accepts special characters in the name input.
        """
        special_names = [
            "John Doe",
            "O'Connor",
            "Smith-Jones",
            "María#123",
        ]

        for name in special_names:
            response = hello_world_client.hello(
                name=name,
                transaction_parameters=p_box_transaction_parameters,
            )
            assert response.return_value == f"Hello, {name}"

    def test_multiple_calls_same_name(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
    ) -> None:
        """
        Checks that repeatedly calling 'hello' with the same name 
        always returns the same greeting.
        """
        name = "Alice"
        expected_greeting = f"Hello, {name}"

        for _ in range(3):
            response = hello_world_client.hello(
                name=name,
                transaction_parameters=p_box_transaction_parameters,
            )
            assert response.return_value == expected_greeting

    def test_input_validation(
        self,
        hello_world_client: HelloWorldClient,
        p_box_transaction_parameters: TransactionParameters,
    ) -> None:
        """
        Expects an exception when passing an excessively long name.
        """
        invalid_name = "A" * 1000

        with pytest.raises(Exception):
            hello_world_client.hello(
                name=invalid_name,
                transaction_parameters=p_box_transaction_parameters,
            )


def ensure_minimum_balance(
    algod_client: AlgodClient,
    funder_account: Account,
    target_address: str,
    required_min: int,
) -> None:
    """
    Ensures that 'target_address' has at least 'required_min' microAlgos 
    by funding it if necessary.
    """
    info = algod_client.account_info(target_address)
    current_balance = info["amount"]
    if current_balance < required_min:
        diff = required_min - current_balance
        sp = algod_client.suggested_params()
        pay_txn = PaymentTxn(
            sender=funder_account.address,
            receiver=target_address,
            amt=diff,
            sp=sp,
        )
        signed_pay = pay_txn.sign(funder_account.private_key)
        algod_client.send_transaction(signed_pay)
