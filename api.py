import responder

api = responder.API()


@api.route("/")
async def hello_world(req, resp):
    try:
        media = await req.media(format="files")
        resp.text = str(media)
    except Exception:
        resp.text = "no files"


def main():
    api.run()


if __name__ == "__main__":
    main()
