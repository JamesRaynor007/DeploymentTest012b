from fastapi import FastAPI, HTTPException, Request
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'FuncionScore.csv')

app = FastAPI()

# Cargar el DataFrame una vez al iniciar la aplicación
df = pd.read_csv(file_path)
print(df.head())  # Verifica las primeras filas del DataFrame

@app.get("/", response_model=dict)
def read_root(request: Request):
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    return {
        "message": "Bienvenido a la API de películas.<br>",
        "instructions": (
            "Usa el endpoint /score/?title=nombre_de_la_pelicula para obtener datos de una película específica.<br>"
            "Por ejemplo: /score/?title=Toy%20Story.<br>"
            "O usa /titles para obtener el listado de películas.<br>"
            "Por ejemplo: /titles.<br>"
        ),
        "links example": [
            {"title": "Toy Story", "url": f"{base_url}/score/?title=Toy%20Story"},
            {"title": "Listado de películas", "url": f"{base_url}/titles"}
        ]
    }    
@app.get("/score/")
async def get_movie(title: str):
    print(f"Buscando película: '{title}'")  # Muestra el título buscado
    movie = df[df['title'].str.lower() == title.lower()]
    print(f"Películas encontradas: {movie}")  # Muestra el DataFrame encontrado

    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_data = movie.iloc[0]
    return {
        "title": movie_data['title'],
        "release_date": int(movie_data['release_year']),  # Convertir a int
        "vote_average": float(movie_data['vote_average'])  # Convertir a float
    }

@app.get("/titles/")
async def get_titles():
    print("Llamando al endpoint /titles/")  # Para diagnóstico
    return df['title'].tolist()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Instrucciones para ejecutar la aplicación:
# Ejecutar en la terminal: uvicorn main:app --reload
