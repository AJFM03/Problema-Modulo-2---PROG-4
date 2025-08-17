import sqlite3

# =============================
#   CONFIGURACIÓN DE BASE DE DATOS
# =============================
def crear_tabla():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL CHECK(estado IN ('leído','no leído'))
        )
    """)
    conn.commit()
    conn.close()


# =============================
#   FUNCIONES CRUD
# =============================

def agregar_libro(titulo, autor, genero, estado):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)",
                   (titulo, autor, genero, estado))
    conn.commit()
    conn.close()
    print("✅ Libro agregado correctamente.")


def actualizar_libro(id_libro, campo, nuevo_valor):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE libros SET {campo} = ? WHERE id = ?", (nuevo_valor, id_libro))
    conn.commit()
    if cursor.rowcount == 0:
        print("⚠️ No se encontró un libro con ese ID.")
    else:
        print("✅ Libro actualizado correctamente.")
    conn.close()


def eliminar_libro(id_libro):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conn.commit()
    if cursor.rowcount == 0:
        print("⚠️ No se encontró un libro con ese ID.")
    else:
        print("✅ Libro eliminado correctamente.")
    conn.close()


def ver_libros():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conn.close()

    if libros:
        print("\n📚 LISTADO DE LIBROS:")
        for libro in libros:
            print(f"[{libro[0]}] '{libro[1]}' - {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
    else:
        print("📭 No hay libros registrados.")


def buscar_libros(campo, valor):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM libros WHERE {campo} LIKE ?", (f"%{valor}%",))
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        print("\n🔍 RESULTADOS DE BÚSQUEDA:")
        for libro in resultados:
            print(f"[{libro[0]}] '{libro[1]}' - {libro[2]} | Género: {libro[3]} | Estado: {libro[4]}")
    else:
        print("⚠️ No se encontraron coincidencias.")


# =============================
#   MENÚ PRINCIPAL
# =============================
def menu():
    crear_tabla()
    while True:
        print("\n====== 📚 MENÚ BIBLIOTECA ======")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Género: ")
            estado = input("Estado (leído / no leído): ").lower()
            if estado not in ("leído", "no leído"):
                print("⚠️ Estado inválido.")
            else:
                agregar_libro(titulo, autor, genero, estado)

        elif opcion == "2":
            ver_libros()
            id_libro = input("ID del libro a actualizar: ")
            print("Campos: titulo, autor, genero, estado")
            campo = input("Campo a actualizar: ").lower()
            nuevo_valor = input("Nuevo valor: ")
            actualizar_libro(id_libro, campo, nuevo_valor)

        elif opcion == "3":
            ver_libros()
            id_libro = input("ID del libro a eliminar: ")
            eliminar_libro(id_libro)

        elif opcion == "4":
            ver_libros()

        elif opcion == "5":
            print("Buscar por: titulo, autor, genero")
            campo = input("Campo: ").lower()
            valor = input("Valor de búsqueda: ")
            buscar_libros(campo, valor)

        elif opcion == "6":
            print("👋 Saliendo del programa. ¡Hasta pronto!")
            break

        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()
