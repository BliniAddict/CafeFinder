import requests
import winsdk.windows.devices.geolocation as wdg

class Model:
    def __init__(self):
        self.query = ""

    async def get_location(self):
        try:
            locator = wdg.Geolocator()
            pos = await locator.get_geoposition_async()
            location = pos.coordinate.latitude, pos.coordinate.longitude
        except:
            location = [52.457878, 13.452590]  #Koordinaten des OSZIMT
        finally:
            return location

    def build_json(self, loc, types, diets, payments):
        self.query = f"""
        [out:json];
        ("""
        
        for key, value in types:
            if (value):
                amenity = key.lower().replace(" ", "_")
                
                self.query += f"""
                node["amenity"="{amenity}"]"""
                
                #region diet
                for key, value in diets:
                    if (value):
                        diet = "diet:"
                        if (key == "Vegetarisch"):
                            diet += "vegetarian"
                        elif (key == "Koscher"):
                            diet += "kosher"
                        else:
                            diet += key.lower()
                        
                        self.query += f"""
                        ["{diet}"="yes"]"""
                #endregion
                #region payment
                for key, value in payments:
                    if (value):
                        payment = "payment:"
                        if (key == "Bargeld"):
                            payment += "cash"
                        elif key == "Karte":
                            payment += "cards"
                        
                        self.query += f"""
                        ["{payment}"="yes"]"""
                #endregion
                        
                self.query += f"""(around:{2000},{loc[0]},{loc[1]});"""
        

    def get_cafes(self):        
        self.query += f""");
        out;
        """

        response = requests.get("https://lz4.overpass-api.de/api/interpreter", params={'data': self.query})
        if response.status_code == 200:
            return response.json()["elements"]
        else:
            print("Fehler beim Abrufen der Daten:", response.status_code)




