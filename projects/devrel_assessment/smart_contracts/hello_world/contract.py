from algopy import (
    ARC4Contract,
    String,
    UInt64,
    subroutine,
    Txn,
    BoxMap,
    log,
)
from algopy.arc4 import abimethod, Address


class HelloWorld(ARC4Contract):
    """
    A simple Hello World smart contract that demonstrates string handling and box storage
    """
    def __init__(self) -> None:
        self.p_box = BoxMap(Address, String, key_prefix=b"p")

    @abimethod()
    def hello(self, name: String) -> String:
        """
        Creates and stores a greeting for the provided name
        Args:
            name: The name to greet
        Returns:
            A greeting phrase including the provided name
        Raises:
            AssertionError: If name is empty or too long
        """
        assert (
            name != String("")
        ), "Name must not be empty"
        assert ( 
            name.bytes.length <= UInt64(128) 
        ), "Name too long. Maximum 128 bytes allowed"
    
        
        greeting = String("Hello, ")
        
        phrase = String("").join((greeting, name))

        log(String("Storing greeting: ").join((phrase,)))

        self.store(phrase)
        
        return phrase

    @subroutine
    def store(self, phrase: String) -> None:
        """
        Stores a greeting phrase in the box map
        Args:
            phrase: The greeting phrase to store
        """
        user_address = Address(Txn.sender)
        self.p_box[user_address] = phrase
