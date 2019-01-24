def test_hello(client):
    assert client.get("/").data == b"Hello, universe!"
