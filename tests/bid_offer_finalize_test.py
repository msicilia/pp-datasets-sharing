import hashlib
import base58
from web3.auto import w3
from eth_account.messages import encode_defunct
import json
from ecdsa import SigningKey 
from brownie import DatasetBidRegistry, accounts
import pytest
import os
import datetime as dt


@pytest.fixture(scope="module")
def registry():
    '''Deploys a singleton dataset bid registry
    '''
    return accounts[0].deploy(DatasetBidRegistry)



def create_ipfs_multihash(content: bytes):
    ''' Helper function to create IPFS multihashes.
        IPFS uses multihashes with the following format:
        base58(<varint hash function code><varint digest size in bytes><hash function output>)
    '''
    content_hash = hashlib.sha256()
    content_hash.update(content)
    function = int(18).to_bytes(1, byteorder='big')
    size = content_hash.digest_size.to_bytes(1, byteorder='big')
    return base58.b58encode(function + size + content_hash.digest())


def create_signed_claim_hash(dataset_spec_file : str):
    ''' Assembles a claim for a dataset spec file.
        A claim is just a hash from the dataset spec file digitally signed.
    '''
    # The hash from the dataset spec need to be converted to string for JSON serialization.
    data_hash = create_ipfs_multihash(bytes(dataset_spec_file, 'utf-8'))
    # Example signing of the dataset spec hash, it real setting could be associated to a certificate. 
    sk = SigningKey.generate()
    signature = sk.sign(data_hash)
    # Build the claim, transform to string and hash.
    claim = {'dataset_spec_hash': str(data_hash),
             'signature': str(signature)}
    return create_ipfs_multihash(bytes(json.dumps(claim), 'utf-8'))

def test_ownership(registry):
    ''' Tests the contract is Ownable (OpenZeppelin libraries)
    '''
    assert(accounts[0] == registry.owner())

@pytest.mark.order(1)
def test_register(registry):
    '''Tests a single registry of a bid. No IPFS testing involved. 
    '''
    with open(os.path.join(os.path.dirname(__file__), "sample_dataset_spec.json"), 'r') as f:
         spec_file = json.load(f)
    timestamp = (dt.datetime.now() +dt.timedelta(days=60)).isoformat()
    tx = registry.register(timestamp, 
                        create_signed_claim_hash(str(spec_file)),
                        1000,
                        "SNOMED_ID:394732004", 
                        {'from': accounts[1]}
                      )
    expiry_date, hash_spec, amount, tag = registry.bidinfo(tx.events[0]['who'], tx.events[0]['position'])
    assert(expiry_date==timestamp)
    assert(amount==1000)    

@pytest.mark.order(2)
def test_offer(registry):
    '''Test the offer for a given bid.
    '''
    # Offer from account[2] 
    tx = registry.offer(accounts[2], accounts[1], 0, 1005)
    offerer, bidder, bid_number, offer_number, value = tx.events[0].values()
    assert(offerer==accounts[2])
    assert(bidder==accounts[1])
    assert(value==1005)

@pytest.mark.order(3)
def test_finalize(registry):
    '''Test the finalization of an offer.
    '''
    before = accounts[2].balance()
    tx = registry.finalize(accounts[2], 0, 0, {'from': accounts[1], 'amount':1005})
    after = accounts[2].balance()
    assert(after == before + 1005)