import requests
import pandas as pd
import os

# URL til shotmap-data for event 13638597
url = "https://www.sofascore.com/api/v1/event/13638597/shotmap"

# Samme headers som i din cURL-kommando
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'baggage': 'sentry-environment=production,sentry-release=svEKXIsCQ5aVRxZbPHRQk,sentry-public_key=d693747a6bb242d9bb9cf7069fb57988,sentry-trace_id=89f51be8effa03c8d3c4a3115fb0fac7',
    'cache-control': 'max-age=0',
    'if-none-match': '"9923732d5a"',
    'priority': 'u=1, i',
    'referer': 'https://www.sofascore.com/da/football/match/randers-fc-fc-kobenhavn/JAsbB',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '89f51be8effa03c8d3c4a3115fb0fac7-bdf9dd99e68e0038',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'bccc28'
}

# Cookie-strengen defineret med triple quotes
cookies_str = """_lr_env_src_ats=false; _ga=GA1.1.955922899.1742818070; gcid_first=882bdaed-ec9e-44c0-9df8-fc9cbd995c5b; FCCDCF=%5Bnull%2Cnull%2Cnull%2C%5B%22CQOxkUAQOxkUAEsACBENBiFoAP_gAEPgAA6IKkAB5C5GTSFBYT51KIsEYAEHwAAAIsAgAgYBAwABQJKU4IQCBGAAEAhAhiICkAAAKlSBIAFACBAQAAAAAAAAIAAEIAAQgAAIICAAAAAAAABICAAoAIoAEAAAwDiABAUA0BgMANIISNyQCQAABSAAQgAAEACAAQAAAEhAAAEIIAAIECgEEIBAGAAAEEEYABlMhAAoIAgAAAAAQAgAQCQBRQACgAAEADwgABAMFRwA8hciJpCgsBwqkEWCEACL4AAAEWAQAAMAwYAAoElKcEIBCjAAAAQAABEACAAAESoAkACAAAwAAAAAAAAAEAASAAAIQAAEEBAAABAAAAAgAAAEAEUACAAAYBQAAgKAYIQGAGkAJC5IBIAQApAAIUAACABAAIAAACQgAACAEAAECAAACEAgDAAACAAIAAymQgAQEAAAAAAAIAQAIBIQogABAAAAABoQAAAEAAA.dngACAAAAAA%22%2C%222~55.70.89.108.135.147.149.184.211.259.313.314.358.415.442.486.540.621.938.981.1029.1031.1033.1046.1092.1097.1126.1205.1268.1301.1514.1516.1558.1579.1584.1598.1651.1697.1716.1753.1810.1832.1859.1985.1987.2010.2068.2069.2140.2224.2271.2282.2316.2328.2373.2387.2440.2571.2572.2575.2577.2628.2629.2642.2646.2650.2657.2677.2767.2778.2822.2860.2878.2887.2889.2922.2970.3169.3182.3190.3194.3215.3226.3234.3290.3292.3300.3330.3331.4631.10631.14332.28031.29631~dv.%22%2C%22CFDDA376-3000-46B8-905E-6A532D7CAE80%22%5D%5D; _cc_id=3cba0eabf8fcb3b899f31c6bbd55bbda; connectId={\"ttl\":86400000,\"lastUsed\":1742818071385,\"lastSynced\":1742818071385}; gc_session_id=gf8ixr49147msab7lamypi; cto_bundle=3cjgs19IYU5OR052VmhpZDk2UmpEdXhBdlNURTlCMlRMWlVDUUZGJTJCJTJCOWVNeThCYVEydyUyRnp4dG1mZ2FtMTBYWlolMkJTb3dsTWZzMm5iYzFnZlVNSzlXZ0FxWEVVRCUyRnZvUkxlWTZIdHBnQWxPeGVrWkFLVyUyQnU1MUN6T1ByQWtURHNnNmZnQXh6WHElMkY1MHJhWjR1ZmlWQnJMNGh1azVhOXd3eHhyUUNFZ1ZGUWQlMkJkNmZLNyUyQmhoTUlHWDlhZGpRcjBDeTAlMkZ2VGpBdzQ0a2prMkFURHI5NGM2QUlteXclM0QlM0Q; FCNEC=%5B%5B%22AKsRol-uLrw7yItq8hd47o85QhojiKSJ_S3qbFzY2mt8PB6fsrmlucUvVUh3dyGnmy52IXIOzObrBfP6Lm5IhP2VIocrJzdlok_1Z2TYKxDRjASHZPsozDZ02pD5M9fL7xtlLGULRTZpLDOnovSEhaCfD-4BipkCVQ%3D%3D%22%5D%5D; _ga_HNQ9P9MGZR=GS1.1.1743527537.13.1.1743529016.60.0.0; __gads=ID=1ef54ca32ed28a5a:T=1742818071:RT=1743529017:S=ALNI_Ma9VK0Y3pTpjR9Bnul9hJ3U6jJbgw; __gpi=UID=0000106dc95d1b3a:T=1742818071:RT=1743529017:S=ALNI_MbsFs_TlX140IAAjlRVKiRIFzL3Zw; __eoi=ID=19faf30e8787673fT=1742818071:RT=1743529017:S=AA-Afja_fy9W1j8iQsmXSOIngKsF"""

# Konverter cookie-strengen til en dictionary
cookies = {}
for part in cookies_str.split(";"):
    if "=" in part:
        name, value = part.split("=", 1)
        cookies[name.strip()] = value.strip()

# Udfør GET-anmodningen med headers og cookies
response = requests.get(url, headers=headers, cookies=cookies)
print("Statuskode:", response.status_code)

# Forsøg at parse JSON-svaret
try:
    data = response.json()
except Exception as e:
    print("Kunne ikke parse JSON:", e)
    data = {}

# Udskriv nøglerne i det modtagne JSON
print("Nøgler i JSON-svaret:", list(data.keys()))

# Forsøg at udtrække shotmap-data
shots = []
if "shotmap" in data:
    shotmap_data = data["shotmap"]
    print("Type af shotmap_data:", type(shotmap_data))
    if isinstance(shotmap_data, dict):
        print("Nøgler i shotmap_data:", list(shotmap_data.keys()))
        if "shots" in shotmap_data:
            shots = shotmap_data["shots"]
        else:
            shots = [shotmap_data]
    elif isinstance(shotmap_data, list):
        shots = shotmap_data

# Hvis shotdata findes, gemmes de i en CSV-fil i mappen "test" på din Desktop
if shots:
    # Bestem stien til mappen "test" på Desktop
    output_dir = os.path.expanduser("~/Desktop/test")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "shotmap_data.csv")
    
    df = pd.DataFrame(shots)
    df.to_csv(output_file, index=False)
    print(f"Data gemt som '{output_file}'")
else:
    print("Ingen shotmap-data fundet")
