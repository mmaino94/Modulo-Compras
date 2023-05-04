import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def read_files():
    proveedores = pd.read_csv("./src/data/proveedores.csv")
    materiales = pd.read_csv("./src/data/materiales1.csv")

    return proveedores, materiales

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
    mensaje['From'] = 'mmaino@meditecna.com.ar'
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Solicitud de cotización'
    mensaje.attach(MIMEText(cuerpo_mensaje, 'html'))

    # Enviar el mensaje
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
        server.starttls()
        direccion_correo = input('Ingrese su dirección de correo electrónico: ')
        contraseña = input('Ingrese su contraseña: ')
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
        proveedores_grupos = {}
        for mat in proveedores['Material'].unique():
            #add key and value to dictionary
            proveedores_grupos[mat] = proveedores[proveedores['Material']==mat]['Mail']
        # Creamos una lista vacía para los grupos de materiales que no tienen proveedores asociados
        grupos_sin_proveedor = []

        # Recorrer la tabla de ejemplo de materiales y agregar cada grupo de materiales único a la lista de grupos seleccionados

        grupos_seleccionados = []

        for grupo in materiales['Grupo'].unique():
            grupos_seleccionados.append(grupo)

        #creo un email con cada grupo de materiales y sus cantidades
        mensajes = {}

        for grupo in grupos_seleccionados:
            materiales_grupo = materiales[materiales['Grupo'] == grupo]
            materiales_grupo = materiales_grupo[['Material', 'Cantidad']]
            materiales_grupo = materiales_grupo.reset_index(drop=True)
            mensajes[grupo] = crear_cuerpo_mensaje(materiales_grupo)

        for grupo in grupos_seleccionados:
            destinatarios = proveedores_grupos[grupo].tolist()
            for des in destinatarios:
                enviar_correo(des, mensajes[grupo])
                print("Email enviado a " + des + " con el grupo " + grupo)
    

    except Exception as e:
        print(e)
        print("Error al leer los archivos")
        exit(1)

    