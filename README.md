# Privacy-preserving blockchain market proof of concept

This is a proof of concept implementation of a mechanism for disclosing requests for anonymized datasets in a network of participants. A typical setting would be that of some **data custodians** (e.g. hospitals or clinics) and a number of **data customers** (e.g. pharma companies or other). 

The core idea is that data customers express preferences using digitally signed *claims* which express the need for a dataset with some given characteristics, set some intended price, and refer to *dataset specs* that detail the requirments. Specs are intended to be stored using some decentralized file system as IPFS, since they may be verbose. Then, data custodians become aware of the needs and elaborate the anonymized dataset from patient data taking into account the risk preferences of those patients. Eventually, custodians match needs with those requirements and are able to *offer* the dataset for a given bid, which can be finalized by the bidder. 

The benefits of using a blockchain setting here include:

* The registering of bids and offers provides transparency and auditability to the process, and the use of DIDs (decentralized identifiers) for the parties involved in the transfer enable the use of P2P secure transfer in a decentralized way. The fact that transfers are committed gets registered immutably in the blockchain, but no patient data is on-chain. This allows for traceability of transfers of datasets, supporting regulatory data protection policies.
* The behaviour of custodians regarding price acceptance or new price proposals provides the required spread of information in the network that is necessary for creating a market, that is driven by demand but reflect the preferences of patients, that are aggregated by custodians. 
* The use of hashes and digital sigantures for claims and data specs function in a similar way as Ricardian contracts, so that the prose of the specs can be considered part of the commonly agreed commitment between the parties. 
* Claims, offers and prices are stored on-chain, but the specs are not, reducing storage needs. Since specs are stored in a decentralized file system, outdated specs might be discarded by the network, or retained only by interested parties.  

## Implementation

The smart contract and tests are developed using the [Brownie framework](https://eth-brownie.readthedocs.io/en/stable/). The design is intended for permissioned, consortium blockchains, so that the deployment would use one of the Ethereum enterprise implementations, as Hyperledger Besu.

It should be noted that this repo contains the smart contract for expressing data needs and offers, but the eventual tranfer is intended to be done using some combination of DIDs and P2P secure transfer, as provided for example by the combination of Hyperledger Indy + Hyperledger Aries. 

## Additional dependencies

In addition to the dependencies used by Brownie, the tests require the following:

* `base58==2.1.0`
* `pytest-order==0.11.0`
* `ecdsa==0.16.1`
## More info

The complete design is in the document:
 
* Rodríguez García, M., Sicilia, M.A. & Dodero, J.M. (2021) *A privacy preserving design for sharing demand-driven patient datasets over permissioned blockchains and P2P secure transfer* (unpublished manuscript).
