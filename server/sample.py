from server.utils import api_process


class SampleAPI:
    def __init__(self):
        pass

    @api_process
    async def info(self, request):
        return {
            "type": "json",
            "key": "value"
        }

    @api_process
    async def stats(self, request):
        return "This is statical data" + str(request)

    @api_process
    async def data(self, request):
        print(request.url)
        data = bytearray()
        while True:
            chunk = await request.content.read(100)
            if not chunk:
                break
            data += chunk
        print(data)
        return True