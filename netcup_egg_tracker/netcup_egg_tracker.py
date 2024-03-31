import requests
import json
import time
import os

refs = [
    "/vserver/vserver_images.php",
    "/vserver/vps.php",
    "/vserver/",
    "/vserver/root-server-erweiterungen.php",
    "/",
    "/hosting",
    "/bestellen/domainangebote.php",
    "/ssl-zertifikate/",
    "/ueber-netcup/",
    "/ueber-netcup/hardware-infrastruktur.php",
    "/ueber-netcup/ddos-schutz-filter.php",
    "/ueber-netcup/auszeichnungen.php"
]

def get_price_formatted(price):
    # Formatieren Sie den Preis, damit er in den Dateinamen eingefügt werden kann
    return price.replace(",", ".").replace("&euro;", "EUR").replace(" ", "")

def main():
    while True:
        for r in refs:
            try:
                resp = requests.post("https://www.netcup.de/api/eggs", data={"requrl": r})
                egg = json.loads(resp.text)["eggs"][0]
                print(egg)
                price = get_price_formatted(egg["price"])
                name = f"{price}Euro_{egg['id']}__{egg['title']}.json"
                name = name.replace("/", "_").replace("|", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_")
                folder_path = "eggs"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                egg['original_url'] = f"https://www.netcup.de/bestellen/produkt.php?produkt={egg['product_id']}&ref=230003&hiddenkey={egg['product_key']}"
                with open(os.path.join(folder_path, name), "w") as file:
                    json.dump(egg, file, indent=4)
            except Exception as e:
                print(f"Error: {e}")
        print(f"\n\n Time Sleep - {2*60}")
        time.sleep(2 * 60)

if __name__ == "__main__":
    main()
