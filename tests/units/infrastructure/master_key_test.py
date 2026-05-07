def test_master_key_parser_valid():
    from src.infrastructure.config.secret_parser import MasterKeyParser

    parser = MasterKeyParser()

    raw = b"v1|2026-01-01T00:00:00+00:00|algo|nonce|deadbeef"

    key = parser.parse(raw)

    assert key.version == "v1"
    assert key.algorithm == "algo"
    assert key.key_hex == "deadbeef"