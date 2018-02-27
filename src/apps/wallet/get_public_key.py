from trezor.messages.HDNodeType import HDNodeType
from trezor.messages.PublicKey import PublicKey
from apps.common import coins, seed


async def get_public_key(ctx, msg):
    coin_name = msg.coin_name or 'Bitcoin'

    node = await seed.derive_node(ctx, msg.address_n)
    coin = coins.by_name(coin_name)

    node_xpub = node.serialize_public(coin.xpub_magic)
    node_type = HDNodeType(
        depth=node.depth(),
        child_num=node.child_num(),
        fingerprint=node.fingerprint(),
        chain_code=node.chain_code(),
        public_key=node.public_key())
    return PublicKey(node=node_type, xpub=node_xpub)
