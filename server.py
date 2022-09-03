from aiohttp import web, ClientSession

default_service = "yandex"

services = {
    "yandex": "https://favicon.yandex.net/favicon/v2/{}",
    "google": "https://www.google.com/s2/favicons?domain_url={}",
    "ddg": "https://icons.duckduckgo.com/ip3/{}.ico",
}


async def get_favicon_bytes(request):
    service_url = request.match_info.get("service_url", default_service)
    domain_url = request.match_info.get("domain_url", None)

    async with ClientSession() as session:
        print(service_url)
        async with session.get(services[service_url].format(domain_url)) as resp:
            print(services[service_url].format(domain_url))
            image_bytes = await resp.read()
    return image_bytes


async def get_favicon(request):
    image = await get_favicon_bytes(request)
    return web.Response(body=image, content_type="image/x-ico")


app = web.Application()
app.router.add_get("/{service_url}/{domain_url}", get_favicon, name="choose_service")
app.router.add_get("/{domain_url}", get_favicon, name="default_service")
web.run_app(app, port=4000)
