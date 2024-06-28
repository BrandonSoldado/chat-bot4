from flask import Flask, request, session, make_response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from bbdd import *
from flask import jsonify
from PromptIA import *
from langchain_groq import ChatGroq
from nemoguardrails.llm.providers import register_llm_provider
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from  bbdd import *
from ast import literal_eval
from azure.storage.blob import BlobServiceClient, BlobClient
from reportlab.lib.enums import TA_CENTER


def SubirPDFazure():
    connect_str = "DefaultEndpointsProtocol=https;AccountName=topichatbot2;AccountKey=mZoW1LahODxmXTdjVIUSv5+w+wXojxVEWbUi6s9LilvzGNZ6IPSJ2v7NTD14mqSwH+0KVIWvp7iz+AStDSzaUA==;EndpointSuffix=core.windows.net"
    container_name = "pdf"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    local_file_name = "factura_proforma.pdf"
    blob_name = "factura_proforma.pdf"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data)


def ObtenerURLpdf():
    account_name = "topichatbot2"
    container_name = "pdf"
    file_name = "factura_proforma.pdf"
    file_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{file_name}"
    return file_url

def EliminarPDFplataforma():
    connect_str = "DefaultEndpointsProtocol=https;AccountName=topichatbot2;AccountKey=mZoW1LahODxmXTdjVIUSv5+w+wXojxVEWbUi6s9LilvzGNZ6IPSJ2v7NTD14mqSwH+0KVIWvp7iz+AStDSzaUA==;EndpointSuffix=core.windows.net"
    container_name = "pdf"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    local_file_name = "factura_proforma.pdf"
    blob_name = "factura_proforma.pdf"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.delete_blob()

def EnviarPDF(telefono, url):

    account_sid = 'ACd1d0ec5e8965f4560d02b1d686992a18'
    auth_token = '1cf39bb2975f712c028aa6f75f4f4430'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        to=telefono,
        media_url=[url]
    )

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Quiero que me devolvas una lista en python sobre los productos que menciona en la pregunta que hace el usuario, solo la lista sin mas texto"),
    ("system", """estos son los productos y sus precios que tenemos:
    productos = [
    ["HG Antimoho", 40.99],
    ["Muffyxid", 30.50],
    ["SaniCentro eliminador de moho", 19.99],
    ["Idroless 2 Lts", 14.75],
    ["Spray limpiador y eliminador de moho y verdin", 30.25],
    ["MPL limpiador antimoho 500ml", 50.00],
    ["Limpiador Antihongos great Value de 1L", 60.00],
    ["LIMPIADOR DE MOHO 85 GLADIO FM CON PULVERIZADOR 500 ML", 100.00],
    ["NUNCAS Spray Antimoho", 25.00],
    ["HARPIC Limpiador Líquido Baños Antihongos", 20.99],
    ["SPRAY ANTIMOHO STOP JUNTAS NEGRAS", 20.99],
    ["Aerosol Antimoho W, Limpiador De Moho, Limpieza Antimoho Cz8", 29.99],
    ["Spray Antimoho Tixol", 25.99],
    ["ANTIMOHO Para superficies afectadas por humedad", 20.00],
    ["FILA Solutions Antimoho", 35.00],
    ["RIMUOVI MUFFA antimoho", 120.00],
    ["Limpiador antimoho", 30.99],
    ["CVR Limpiador antimoh", 50.99]"""),
    ("system", """estos son los productos y sus precios que tenemos en oferta:
    productos_oferta = [
    ["HG Antimoho", 36.89],
    ["Muffyxid", 27.45],
    ["SaniCentro eliminador de moho", 17.99],
    ["Idroless 2 Lts", 13.27],
    ["Spray limpiador y eliminador de moho y verdin", 27.23],
    ["MPL limpiador antimoho 500ml", 45.00],
    ["Limpiador Antihongos great Value de 1L", 54.00],
    ["LIMPIADOR DE MOHO 85 GLADIO FM CON PULVERIZADOR 500 ML", 90.00],
    ["NUNCAS Spray Antimoho", 22.50]
    ]"""),
    ("system", """La lista que me vas a dar quiero que tenga este formato:
    [["ID", "Producto", "Cantidad", "Precio(Bs)", "Total(Bs)"],
    ["1", "Producto1", "1", "100.00", "100.00"],
    ["2", "Producto2", "3", "100.00", "300.00"],
    ["3", "Producto3", "2", "100.00", "200.00"] ....
    ]"""),
    ("system", "Solo dame la lista sin mas texto ni detalle, en el formato que te di"),

    ("human", "{pregunta}")
])

prompt3 = ChatPromptTemplate.from_messages([
    ("system", "Si algun producto no esta en la pregunta que te doy, eliminalo, compara con la lista que te he dadd"),
    ("system", """Esta es la lista de los productos que tenes que verificar:
    [HG Antimoho,
    Muffyxid,
    SaniCentro eliminador de moho,
    Idroless 2 Lts,
    Spray limpiador y eliminador de moho y verdin,
    MPL limpiador antimoho 500ml,
    Limpiador Antihongos great Value de 1L,
    LIMPIADOR DE MOHO 85 GLADIO FM CON PULVERIZADOR 500 ML,
    NUNCAS Spray Antimoho,
    HARPIC Limpiador Líquido Baños Antihongos,
    SPRAY ANTIMOHO STOP JUNTAS NEGRAS,
    Aerosol Antimoho W, Limpiador De Moho, Limpieza Antimoho Cz8,
    Spray Antimoho Tixol,
    ANTIMOHO Para superficies afectadas por humedad,
    FILA Solutions Antimoho,
    RIMUOVI MUFFA antimoho,
    Limpiador antimoho,
    CVR Limpiador antimoh]"""),


    ("human", "{pregunta}")
])



















def generate_proforma_invoice(filename, producto):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=22, alignment=TA_CENTER, textColor=colors.orange)
    title_text = Paragraph("FACTURA PROFORMA", title_style)
    elements.append(title_text)
    elements.append(Spacer(1, 50))

    info_style = styles['Normal']

    # Factura de, Factura a y N° Factura
    header_data = [
        [Paragraph("Factura de: Proforma<br/>Empresa / Autónomo: Anonima<br/>Domicilio: Anonina<br/>Identificación fiscal: XAXX010101000<br/>Ciudad, código postal: SCZ, 28039", info_style),
         Paragraph("Factura a: Miguel<br/>Empresa / Autónomo: Anonima<br/>Domicilio: Anonima<br/>Identificación fiscal: XAXX010100000<br/>Ciudad, código postal: SCZ, 28034", info_style),
         Paragraph(f"N° Factura: 0001<br/>Fecha emisión: {datetime.now().strftime('%Y-%m-%d')}<br/>", info_style)]
    ]

    header_table = Table(header_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Tabla de productos/servicios
    data = producto
    # Subtotal, IRPF, IVA y Total
    total = 0.0
    for fila in producto:
        if fila[0].isdigit():  # Verifica que la primera columna sea un número (ID)
            total += float(fila[4])
    data.insert(0, ["ID", "Producto", "Cantidad", "Precio(Bs)", "Total(Bs)"])

    # Estilo para las celdas de nombres de productos
    product_name_style = ParagraphStyle(
        name='Product Name',
        fontSize=10,  # Tamaño de la fuente reducido a 10 puntos
        textColor=colors.black
    )

    # Crear tabla de productos/servicios con estilos personalizados
    table = Table(data, colWidths=[1*inch, 2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    for row_idx in range(len(data)):
        for col_idx in range(len(data[row_idx])):
            if row_idx == 0:  # Primera fila (encabezados)
                cell_style = TableStyle([
                    ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.orange),
                    ('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.whitesmoke),
                    ('ALIGN', (col_idx, row_idx), (col_idx, row_idx), 'CENTER'),
                    ('FONTNAME', (col_idx, row_idx), (col_idx, row_idx), 'Helvetica-Bold'),
                    ('FONTSIZE', (col_idx, row_idx), (col_idx, row_idx), 12),
                    ('BOTTOMPADDING', (col_idx, row_idx), (col_idx, row_idx), 12),
                    ('GRID', (col_idx, row_idx), (col_idx, row_idx), 1, colors.black)
                ])
            else:  # Filas de datos
                cell_style = TableStyle([
                    ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.whitesmoke),
                    ('ALIGN', (col_idx, row_idx), (col_idx, row_idx), 'CENTER'),
                    ('FONTNAME', (col_idx, row_idx), (col_idx, row_idx), 'Helvetica'),
                    ('FONTSIZE', (col_idx, row_idx), (col_idx, row_idx), 10),
                    ('GRID', (col_idx, row_idx), (col_idx, row_idx), 1, colors.black)
                ])
                if col_idx == 1:  # Columna de nombres de productos
                    cell_style.add('FONTSIZE', (col_idx, row_idx), (col_idx, row_idx), 8)  # Ajustar tamaño para nombres de productos

            table.setStyle(cell_style)

    elements.append(table)
    elements.append(Spacer(1, 20))
    
    totals_data = [
        ["", "", "", "Subtotal", str(total) + " Bs"],
        ["", "", "", "IRPF 15%", str(total*0.15) + " Bs"],
        ["", "", "", "IVA 21%", str(total*0.21) + " Bs"],
        ["", "", "", "Total", "{:.3f} Bs".format(total - (total*0.15) + (total*0.21))]
    ]

    totals_table = Table(totals_data, colWidths=[1*inch, 2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (-1, -1), (-1, -1), colors.orange),
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.whitesmoke)
    ]))

    elements.append(totals_table)
    elements.append(Spacer(1, 20))

    # Información adicional y pie de página
    footer_text = Paragraph("Por favor haga el pago a", styles['Normal'])
    elements.append(footer_text)
    elements.append(Spacer(1, 12))

    footer_data = [
        ["Email: pagoonline@gmail.com"],
        ["Referencia: 238918.23SD"]
    ]

    footer_table = Table(footer_data, colWidths=[4.5*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(footer_table)
    
    # Guardar PDF
    doc.build(elements)
