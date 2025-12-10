package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Estructura para representar un álbum.
type album struct {
	ID     string `json:"id"`
	Title  string `json:"title"`
	Artist string `json:"artist"`
	Year   int    `json:"year"`
}

// Slice en memoria para almacenar los álbumes.
var albums = []album{
	{ID: "1", Title: "Familia", Artist: "camila cabello", Year: 2022},
	{ID: "2", Title: "21", Artist: "Adele", Year: 2012},
	{ID: "3", Title: "the eminem show", Artist: "Eminem", Year: 2002}, // Corregido el año
}

// getAlbums maneja las solicitudes GET a /albums
// Retorna la lista completa de álbumes.

func getAlbums(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums maneja las solicitudes POST a /albums
// Añade un nuevo álbum a la lista.

func postAlbums(c *gin.Context) {
	var newAlbum album

	if err := c.BindJSON(&newAlbum); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	albums = append(albums, newAlbum) // Añade el nuevo álbum al slice.

	// Responde con el slice actualizado y un estado 201 Created.
	c.IndentedJSON(http.StatusCreated, newAlbum) // Mejor devolver solo el álbum creado.
}

// getAlbumsID maneja las solicitudes GET a /albums/:id
// Retorna un álbum específico por su ID.
func getAlbumsID(c *gin.Context) {
	id := c.Param("id") // Obtiene el parámetro 'id' de la URL.

	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}

	c.JSON(http.StatusNotFound, gin.H{"message": "Álbum no encontrado"})
}

// updateAlbum maneja las solicitudes PUT a /albums/:id
// Actualiza un álbum existente por su ID.
func updateAlbum(c *gin.Context) {
	id := c.Param("id") // Obtiene el ID del álbum a actualizar.
	var updatedAlbum album

	// Intenta enlazar el JSON del cuerpo de la solicitud a la estructura updatedAlbum.
	if err := c.BindJSON(&updatedAlbum); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	// Busca el índice del álbum con el ID proporcionado.
	foundIndex := -1
	for i, a := range albums {
		if a.ID == id {
			foundIndex = i
			break
		}
	}

	if foundIndex == -1 {
		c.JSON(http.StatusNotFound, gin.H{"message": "Álbum no encontrado para actualizar"})
		return
	}

	// Actualiza el álbum en el slice.
	// Asegúrate de que el ID no cambie si no quieres que el cliente lo modifique.
	albums[foundIndex] = updatedAlbum
	albums[foundIndex].ID = id // Aseguramos que el ID del álbum actualizado sea el de la URL

	c.IndentedJSON(http.StatusOK, albums[foundIndex]) // Devuelve el álbum actualizado.
}

// deleteAlbum maneja las solicitudes DELETE a /albums/:id
// Elimina un álbum por su ID.

func deleteAlbum(c *gin.Context) {
	id := c.Param("id")

	foundIndex := -1
	for i, a := range albums {
		if a.ID == id {
			foundIndex = i
			break
		}
	}

	if foundIndex == -1 {

		c.JSON(http.StatusNotFound, gin.H{"message": "Álbum no encontrado para eliminar"})
		return
	}

	// Esto crea un nuevo slice excluyendo el elemento en foundIndex.
	albums = append(albums[:foundIndex], albums[foundIndex+1:]...)

	// Responde con un estado 204 No Content, ya que la eliminación fue exitosa y no hay contenido que devolver.
	c.Status(http.StatusNoContent)
}

func main() {
	router := gin.Default()

	// Rutas existentes
	router.GET("/albums", getAlbums)
	router.POST("/albums", postAlbums)
	router.GET("/albums/:id", getAlbumsID)

	// Nuevas rutas para PUT y DELETE
	router.PUT("/albums/:id", updateAlbum)    // Para actualizar un álbum específico
	router.DELETE("/albums/:id", deleteAlbum) // Para eliminar un álbum específico

	// Inicia el servidor
	router.Run("localhost:8080")
}
