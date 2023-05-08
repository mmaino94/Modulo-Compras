import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def read_files():
    proveedores = pd.read_csv(r"C:\Users\mmaino\Desktop\Python\Modulo-Compras\src\data\proveedores.csv")
    materiales = pd.read_csv(r"C:\Users\mmaino\Desktop\Python\Modulo-Compras\src\data\materiales1.csv")

    return proveedores, materiales

# Creamos un diccionario vacio para asociar cada grupo de materiales con sus proveedores
def grupos(proveedores):
    proveedores_grupos = {}

    for mat in proveedores['Material'].unique():
        #add key and value to dictionary
        proveedores_grupos[mat] = proveedores[proveedores['Material']==mat]['Mail']
        
    # Creamos una lista vacía para los grupos de materiales que no tienen proveedores asociados
    grupos_sin_proveedor = []

    # Recorrer la tabla de ejemplo de materiales y agregar cada grupo de materiales único a la lista de grupos seleccionados

    grupos_seleccionados = []

    # Defino los grupos disponibles en la lista de materiales
    
    grupos_disponibles = materiales['Grupo'].unique().tolist()


    # Recorrer la tabla de ejemplo de materiales y agregar cada grupo de materiales único a la lista de grupos seleccionados
    for grupo in proveedores['Material'].unique():
        grupos_seleccionados.append(grupo)

    #Generacion de la lista final de grupos
    grupos_final = list(set(grupos_disponibles).intersection(grupos_seleccionados))
    grupos_final
    
        
    for grupo in grupos_disponibles:
        # Verificamos si el grupo tiene proveedor asociado
        if grupo not in proveedores_grupos:
            grupos_sin_proveedor.append(grupo)
            continue

    print(f'Los Grupos que se solicitara cotizacion son: {grupos_final}')
    print(f'No se encontro proveedor para: {grupos_sin_proveedor}')

    # Preguntar si el usuario desea eliminar algún grupo
    eliminar = input('¿Desea eliminar algún grupo? (S/N): ')

    if eliminar.lower() == 's':
        # Solicitar al usuario que ingrese los grupos a eliminar
        eliminar_grupos = input('Ingrese los grupos que desea eliminar (separados por comas): ').split(',')
        # Eliminar los espacios en blanco de los nombres de grupo
        #eliminar_grupos = [grupo.strip() for grupo in eliminar_grupos]

        # Eliminar los grupos seleccionados de la lista de grupos a enviar correo
        for grupo in eliminar_grupos:
            if grupo in grupos_final:
                grupos_final.remove(grupo)
                print(f'Se ha eliminado el grupo {grupo} de la lista de grupos seleccionados.')
            else:
                print(f'El grupo {grupo} no se encontraba en la lista de grupos seleccionados.')
    else:
        print('No se eliminará ningún grupo.')

    return grupos_final
  

#Funcion para crear el mensaje y enviar a los grupos correctos
def mensaje_final(grupos_seleccionados):
    mensajes = {}

    for grupo in grupos_seleccionados:
        materiales_grupo = materiales[materiales['Grupo'] == grupo]
        materiales_grupo = materiales_grupo[['Material', 'Cantidad']]
        materiales_grupo = materiales_grupo.reset_index(drop=True)
        mensajes[grupo] = crear_cuerpo_mensaje(materiales_grupo)

    for grupo in grupos_seleccionados:
        destinatarios = proveedores_grupos[grupo].tolist()
        for des in destinatarios:
            #enviar_correo(des, mensajes[grupo])
            print("Email enviado a " + des + " con el grupo " + grupo)


#create html email body with material and quantities inside a table, the table is created with a for loop from the dataframe

def crear_cuerpo_mensaje(df: pd.DataFrame):
    cuerpo_mensaje = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
    <meta http-equiv="Content-Type" content="text/html charset=UTF-8" />
    <head>
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th {
    background-color: #4CAF50;
    color: white;
    }
    </style>
    </head>
    <body>
    <p>Estimado proveedor, <br><br>
    Por medio de la presente le solicitamos la cotización de los siguientes materiales:<br><br>
    <table style="width:50%">
    <tr>
    <th>Material</th>
    <th>Cantidad</th>
    </tr>
    """
    for index, row in df.iterrows():
        cuerpo_mensaje += """
        <tr>
        <td>""" + row["Material"] + """</td>
        <td>""" + str(row["Cantidad"]) + """</td>
        </tr>
        """
    cuerpo_mensaje += """
    </table>
    <br>
    Quedamos atentos a su respuesta.<br><br>
    Saludos cordiales,<br><br>
    Compras
    </p>
    </body>
    </html>
    """
    return cuerpo_mensaje

def enviar_correo(destinatario: str, cuerpo_mensaje: str):
    # Crear el mensaje
    mensaje = MIMEMultipart()
    direccion_correo = input('Ingrese su dirección de correo electrónico: ')
    contraseña = input('Ingrese su contraseña: ')
    mensaje['From'] = direccion_correo
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Solicitud de cotización'
    mensaje.attach(MIMEText(cuerpo_mensaje, 'html'))

    # Enviar el mensaje
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
        server.starttls()
        direccion_correo = direccion_correo
        contraseña = contraseña
        try:
            server.login(direccion_correo, contraseña)
        except smtplib.SMTPAuthenticationError:
            print('Las credenciales ingresadas son incorrectas. Por favor, inténtelo nuevamente.')
            return
        finally:
            server.sendmail(mensaje['From'], mensaje['To'], mensaje.as_string())
            print('El mensaje se envió correctamente.')
            #close server
            server.quit()



if __name__ == "__main__":
    try:
        proveedores, materiales = read_files()
        print("se leyeron bien los archivos")
        grupos_seleccionados=grupos(proveedores)
        mensaje_final(grupos_seleccionados) 

    except Exception as e:
        print(e)
        print("Error al leer los archivos")
        exit(1)

    