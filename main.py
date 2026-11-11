import flet as ft
import psycopg2
from db import get_products

WHITE = "#FFFFFF"
LIGHT_GREEN = "#D2F6E7"
GREEN = "#70B2AF"
LOW_STOCK="#FF8080"

def product_card(product):
    quantity = product.quantity

    bgcolor = LOW_STOCK if quantity <= 3 else WHITE

    photo = ft.Image(
        src = product.image or "picture.png",
        width = 110,
        height = 110,
        error_content =ft.Image(
            src = product.image or "picture.png",
            width = 110,
            height = 110
        ),
    )
    info = ft.Column(
        controls =  [
            ft.Container(
                content = ft.Text(
                    f'{product.manufacturer} | {product.name}',
                    text_align= ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD
                ),
                alignment=ft.Alignment.TOP_CENTER
            ),
            ft.Text(f"Категория: {product.category}"),
            ft.Text(f"Количество: {product.quantity}"),
            ft.Text(f"Состав: {product.content}")
        ],
        expand = True
    )

    price = ft.Container(
        content = ft.Text(
            f"{product.price:.2f}",
            size = 19,
            weight=ft.FontWeight.BOLD
        ),
        width=125,
        height=110,
        alignment = ft.Alignment.CENTER
    )

    return ft.Container(
        content = ft.Row(
            controls = [photo, info, price]
        ),
        bgcolor =bgcolor,
        border= ft.Border.all(1, LIGHT_GREEN),
        padding = 15
    )

def main(page: ft.Page):
    page.title= "Чудо обувь"
    page.bgcolor = WHITE
    page.theme = ft.Theme(font_family = "Calibri")
    page.padding = 25

    header = ft.Container(
        content=ft.Row(
            [
                ft.Image(src = "icon.png", width= 70, height= 70),
                ft.Text("Каталог обуви", weight = ft.FontWeight.W_700)
            ],
        spacing= 20),
        bgcolor= LIGHT_GREEN,
        border=ft.Border.all(1, LIGHT_GREEN)
    )

    catalog = ft.Column(
        spacing= 12,
        scroll = ft.ScrollMode.AUTO,
        expand = True
    )

    try:
        products = get_products()

        for product in products:
            catalog.controls.append(product_card(product))
        if not products:
            catalog.controls.append(ft.Text("Товары не найденны"))

    except psycopg2.Error:
        catalog.controls.append(ft.Text("Ошибка базы данных:{error}", color ="red"))

    page.add(
        ft.Column(
            controls = [header, catalog],
            spacing = 20,
            expand = True
        )
    )

ft.run (main, assets_dir= "assets")
