from pymongo import MongoClient

#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb+srv://lucia-dos:123456lucia@despliegueflask.vlrjgyf.mongodb.net/?retryWrites=true&w=majority&appName=despliegueFlask")
db = client['examenfebrero']
productos = db['productos']

data = [
    {"nombre": "Laptop Gamer", "descripcion": "Laptop con procesador Intel i7, 16GB RAM y GPU RTX 3060.", "precio": 1500},
    {"nombre": "Mouse Inalámbrico", "descripcion": "Mouse ergonómico con conexión Bluetooth y batería recargable.", "precio": 45},
    {"nombre": "Teclado Mecánico RGB", "descripcion": "Teclado con switches mecánicos y retroiluminación RGB personalizable.", "precio": 80},
    {"nombre": "Monitor 27\" 144Hz", "descripcion": "Monitor IPS de 27 pulgadas con tasa de refresco de 144Hz y resolución 2K.", "precio": 300},
    {"nombre": "Silla Gamer", "descripcion": "Silla ergonómica con reposabrazos ajustables y soporte lumbar.", "precio": 200},
    {"nombre": "Disco SSD 1TB", "descripcion": "Unidad de almacenamiento SSD NVMe de alta velocidad.", "precio": 120},
    {"nombre": "Tarjeta de Video RTX 4070", "descripcion": "GPU NVIDIA RTX 4070 con 12GB de memoria GDDR6.", "precio": 700},
    {"nombre": "Procesador Ryzen 9 7900X", "descripcion": "CPU AMD Ryzen de 12 núcleos y 24 hilos, ideal para gaming y edición.", "precio": 550},
    {"nombre": "Fuente de Poder 850W", "descripcion": "Fuente de poder certificada 80 Plus Gold con cables modulares.", "precio": 130},
    {"nombre": "Auriculares Inalámbricos", "descripcion": "Auriculares con sonido envolvente 7.1 y micrófono con cancelación de ruido.", "precio": 90}
]

productos.insert_many(data)
print("Productos insertados correctamente.")