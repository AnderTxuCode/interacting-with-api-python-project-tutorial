import os
import pandas as pd
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

con = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                            client_secret=client_secret))

# La Bichota
artist_id = "790FomKkXshlbRYZFtlgla"

# Obtener las canciones más populares
response = con.artist_top_tracks(artist_id)

if response:
    tracks = response["tracks"]
    tracks = [{k: (v / (1000 * 60)) % 60 if k == "duration_ms" else v 
               for k, v in track.items() if k in ["name", "popularity", "duration_ms"]} 
              for track in tracks]
    
    for track in tracks:
        print(f"Canción: {track['name']}, Popularidad: {track['popularity']}, Duración: {track['duration_ms']:.2f} minutos")
    
    canciones = pd.DataFrame(tracks)
    
    canciones.rename(columns={'duration_ms': 'Duración', 'name': 'Nombre', 'popularity': 'Popularidad'}, inplace=True)

    ordenado = canciones.sort_values(by='Popularidad', ascending=False)
    top3 = ordenado.head(3)
    print("\nTop 3 por popularidad")
    print(top3)

    # Scatter plot: Duración vs Popularidad
    plt.figure(figsize=(10, 6))
    plt.scatter(canciones['Duración'], canciones['Popularidad'], color='purple', alpha=0.7)
    plt.title('Relación entre Duración y Popularidad de Karol G')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Popularidad')
    plt.grid(True)
    plt.savefig('scatter_plot.png')
    plt.show()

    correlation = canciones['Duración'].corr(canciones['Popularidad'])
    print(f"\nCorrelación entre duración y popularidad: {correlation:.2f}")
    print(f"\nNo hay correlación se puede ver claramente que los puntos están separados, la imagen está en PNG ya que no hay parte visual.")
else:
    print("No hay respuesta")