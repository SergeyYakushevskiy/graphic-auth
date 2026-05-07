def test_file_secret_repository_save_and_load(tmp_path):
    from src.infrastructure.storage import FileSecretRepository

    repo = FileSecretRepository(tmp_path / "shadow.ga")

    repo.save("user1", "bg1", b"\x01\x02\x03")

    loaded = repo.load("user1")

    assert loaded is not None
    assert loaded[0] == "bg1"
    assert loaded[1] == b"\x01\x02\x03"