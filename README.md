## Instalación y ejecución

### 1. Clonar el repositorio

2. Crear el entorno virtual
py -3.12 -m venv .venv
3. Activar el entorno virtual
.venv\Scripts\activate
4. Instalar dependencias
pip install -r requirements.txt
5. Ejecutar la API
uvicorn app.main:app --reload
6. Abrir documentación Swagger
http://127.0.0.1:8000/docs


Para incorporar la funcionalidad de protección de imágenes de la Parte 2, se modificaron principalmente los archivos app/services/cloudinary_service.py, app/services/radiograph_service.py y app/schemas/radiograph.py. En cloudinary_service.py se ajustó la subida de imágenes para que se almacenen en Cloudinary como recursos protegidos (authenticated) y se añadió la lógica base para generar URLs firmadas. En radiograph_service.py se cambió el flujo de carga para guardar el public_id de Cloudinary en lugar de una URL pública fija, dejando preparada la integración para el acceso temporal y restringido. Finalmente, en radiograph.py se actualizó el esquema de respuesta del endpoint de subida de imágenes para reflejar el uso de public_id en vez de image_url.


## Flujo de uso del sistema

### 1. Iniciar sesión con Google
El usuario inicia sesión con Google desde la página de prueba de autenticación

### 2. Copiar el `id_token`
Después del login, Google devuelve un id_token
Ese token se copia para probar el endpoint de autenticación en swagger

### 3. Autenticarse en Swagger
En swagger se utiliza el endpoint:

 POST /auth/google

En el body se pega el id_token de Google

### 4. Obtener el JWT de la API
Si el id_token es válido, la API responde con un access_token 
Ese token corresponde al JWT propio del sistema

### 5. Autorizar en Swagger
El access_token devuelto por la API se copia y se utiliza en el wagger

Con esto ya se pueden consumir los endpoints protegidos

### 6. Crear un paciente
Con el JWT activo, se crea un paciente mediante el endpoint correspondiente

### 7. Crear una radiografía
Luego se registra una radiografía asociada al paciente

### 8. Subir la imagen radiográfica
Se utiliza el endpoint de carga de imagen para asociar el archivo a la radiografía  
La imagen se almacena en cloudinary como recurso protegido

### 9. Esperar el ocultamiento de la radiografía
Según la lógica implementada, la radiografía pasa a estado oculto mediante la tarea programada del sistema

### 10. Solicitar acceso temporal firmado
Cuando la radiografía ya está oculta, se utiliza el endpoint:

 POST /radiographs/{radiograph_id}/signed-url

Este endpoint genera un acceso temporal con expiración de 5 o 10 minutos

### 11. Consultar la imagen protegida
Con el token o acceso temporal generado se utiliza el endpoint:

 GET /radiographs/{radiograph_id}/private-image

Así se obtiene la imagen protegida

### 12. Verificar expiración
Después del tiempo configurado, se vuelve a probar el mismo acceso  
La imagen ya no debería poder consultarse


###  Decisiones tecnicas relevantes

Se utilizó FastAPI como framework principal para el desarrollo de la API
Se utilizó SQLite como base de datos del proyecto
Se utilizó SQLAlchemy el manejo de entidades y persistencia
Se utilizó Alembic para el control de migraciones de base de datos
Se utilizó Google SSO para la autenticación de usuarios
Se utilizó JWT para proteger los endpoints privados de la API
Se utilizó Cloudinary para el almacenamiento externo de imágenes
Las imágenes radiográficas protegidas se manejan mediante recursos autenticados y acceso temporal firmado
Se utilizó una arquitectura por capas para mantener el sistema organizado y facilitar la integración entre módulos
Se integró lógica de ocultamiento de radiografías y acceso temporal firmado, permitiendo que las imágenes solo puedan visualizarse durante un tiempo limitado