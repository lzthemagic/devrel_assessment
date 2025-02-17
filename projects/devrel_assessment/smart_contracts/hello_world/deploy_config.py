import logging

from algokit_utils import (
    TransactionParameters,
    OnSchemaBreak,
    OnUpdate,
    ApplicationSpecification,
    Account,
)
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.transaction import PaymentTxn
from algosdk.encoding import decode_address

logger = logging.getLogger(__name__)

def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: ApplicationSpecification,
    deployer: Account,
) -> None:
    from smart_contracts.artifacts.hello_world.hello_world_client import (
        HelloWorldClient,
    )

    app_client = HelloWorldClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.deploy(
        on_schema_break=OnSchemaBreak.AppendApp,
        on_update=OnUpdate.AppendApp,
    )

    name = "Murilo"

    box_prefix = b"p"
    raw_name_bytes = bytes(name, "utf-8")
    raw_addr_bytes = decode_address(deployer.address) 

    full_key = box_prefix + raw_addr_bytes

    box_cost = calc_box_cost(key_size=len(full_key), value_size=len(raw_name_bytes))
    logger.info(f"Box cost: {box_cost}")

    min_balance = box_cost + 120900
    logger.info(f"Minimum balance: {min_balance}")

    ensure_minimum_balance(algod_client, deployer=deployer, app_address=app_client.app_address, required_min_balance=min_balance)
    
    transaction_parameters = TransactionParameters(
        boxes=[[app_client.app_id, full_key]]
    )

    response = app_client.hello(name=name, transaction_parameters=transaction_parameters)
    logger.info(
        f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
        f"with name={name}, received: {response.return_value}"
    )

def calc_box_cost(key_size: int, value_size: int) -> int:
    return 2500 + 400 * (key_size + value_size)

def ensure_minimum_balance(
    algod_client: AlgodClient,
    deployer: Account,
    app_address: str,
    required_min_balance: int,
):
    # Made to ensure that first run works and show a example of cost calculation. Better balance calculations based on boxes cost and app cost should be made.
    info = algod_client.account_info(app_address)
    current_balance = info["amount"]
    if current_balance < required_min_balance:
        diff = required_min_balance - current_balance
        logger.info(f"Insufficient funds ({current_balance}), sending {diff} microAlgos to {app_address}")
        sp = algod_client.suggested_params()
        pay_txn = PaymentTxn(
            sender=deployer.address,
            receiver=app_address,
            amt=diff,  
            sp=sp
        )
        signed_pay = pay_txn.sign(deployer.private_key)
        txid = algod_client.send_transaction(signed_pay)
        logger.info(f"Transaction sent. ID: {txid}")
