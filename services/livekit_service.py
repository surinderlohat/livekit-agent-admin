from livekit import api


async def get_livekit_client(db_session):
    from database import Config

    url = db_session.query(Config).filter(Config.key == "livekit_url").first().value
    api_key = (
        db_session.query(Config).filter(Config.key == "livekit_api_key").first().value
    )
    api_secret = (
        db_session.query(Config)
        .filter(Config.key == "livekit_api_secret")
        .first()
        .value
    )

    return api.LiveKitAPI(url, api_key, api_secret)


async def list_trunks(db_session):
    lkapi = await get_livekit_client(db_session)
    try:
        # Use the SIP service to list trunks
        res = await lkapi.sip.list_sip_trunk(api.ListSIPTrunkRequest())
        return [
            {
                "id": t.sip_trunk_id,
                "name": t.name,
                "address": t.outbound_address,
                "numbers": t.inbound_numbers,
            }
            for t in res.items
        ]
    finally:
        await lkapi.aclose()


async def list_dispatch_rules(db_session):
    lkapi = await get_livekit_client(db_session)
    try:
        res = await lkapi.sip.list_sip_dispatch_rule(api.ListSIPDispatchRuleRequest())
        return [
            {
                "id": r.sip_dispatch_rule_id,
                "name": r.name,
                "trunk_ids": r.trunk_ids,
                "rule": str(r.rule),
            }
            for r in res.items
        ]
    finally:
        await lkapi.aclose()
