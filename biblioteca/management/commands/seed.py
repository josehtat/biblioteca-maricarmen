import random
from datetime import date
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth.models import User
from biblioteca.models import Categoria, Pais, Llengua, Llibre, Exemplar, Usuari

class Command(BaseCommand):
    help = 'Genera datos de prueba para libros, ejemplares y usuarios'

    def handle(self, *args, **kwargs):
        # Crear categorías de ejemplo
        categories = ['Ficción', 'Ciencia', 'Historia', 'Arte', 'Tecnología']
        categoria_objs = []
        for category in categories:
            categoria_objs.append(Categoria.objects.create(nom=category))

        # Crear países de ejemplo
        paises = ['España', 'Francia', 'Reino Unido', 'Estados Unidos', 'Canadá']
        pais_objs = []
        for pais in paises:
            pais_objs.append(Pais.objects.create(nom=pais))

        # Crear lenguas
        llenguas = ['Català', 'Castellano', 'English', 'Français']
        llengua_objs = []
        for llengua in llenguas:
            llengua_objs.append(Llengua.objects.create(nom=llengua))

        # Crear libros
        idiomas = ['Català', 'Castellano', 'English', 'Français']
        libros = []

        for idioma in idiomas:
            for i in range(10):
                titol = f"Libro {idioma} {i+1}"
                titol_original = f"Original {idioma} {i+1}" if random.choice([True, False]) else ""
                autor = f"Autor {i+1}"
                cdu = f"CDU-{random.randint(100, 999)}"
                signatura = f"SIGN-{random.randint(1, 100)}"
                data_edicio = date(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
                resum = "Resumen del libro" if random.choice([True, False]) else ""
                anotacions = "Anotaciones del libro" if random.choice([True, False]) else ""
                mides = "21x14 cm" if random.choice([True, False]) else ""
                tags = random.sample(categoria_objs, k=random.randint(1, 3))
                
                # Seleccionar lengua y país aleatoriamente
                llengua = Llengua.objects.get(nom=idioma)
                pais = random.choice(pais_objs)
                
                llibre = Llibre.objects.create(
                    titol=titol,
                    titol_original=titol_original,
                    autor=autor,
                    CDU=cdu,
                    signatura=signatura,
                    data_edicio=data_edicio,
                    resum=resum,
                    anotacions=anotacions,
                    mides=mides,
                    llengua=llengua,
                    pais=pais
                )

                # Añadir las categorías (tags)
                llibre.tags.add(*tags)
                libros.append(llibre)

                # Crear dos ejemplares para cada libro
                for j in range(2):
                    Exemplar.objects.create(
                        cataleg=llibre,
                        registre=f"REG-{llibre.id}-{j+1}",
                        exclos_prestec=False,
                        baixa=False
                    )
        
        # Crear usuarios
        for i in range(50):
            username = f"user{i+1}"
            password = "password123"
            email = f"user{i+1}@example.com"
            centre = random.choice(['Centre A', 'Centre B', 'Centre C'])
            cicle = random.choice(['Cicle A', 'Cicle B', 'Cicle C'])
            user = Usuari.objects.create_user(
                username=username,
                password=password,
                email=email,
                centre=centre,
                cicle=cicle
            )

            # Asignar imágenes y tokens de autenticación opcionales
            user.imatge = None  # Puedes agregar una imagen si quieres
            user.auth_token = f"token_{user.id}"
            user.save()

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
