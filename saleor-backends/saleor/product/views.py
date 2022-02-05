import mimetypes
import os
from typing import Union

from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from .models import DigitalContentUrl
from .utils.digital_products import (
    digital_content_url_is_valid,
    increment_download_count,
)

from .models import (
    Category,
    ProductType,
    ProductVariant,
    ProductImage,
    VariantImage,
)


def generate_xml():

    print(f'{MEDIA_URL }/parse.xml')
    file = open(f'{MEDIA_URL }/parse.xml', mode='w+t', encoding='utf-8')

    file.write("< Ads formatVersion = \"3\" target = \"Avito.ru\" >< Ad >")
    file.write("< Id > 723681273 < / Id >")
    file.write("< DateBegin > 2015 - 11 - 27 < / DateBegin >")
    file.write("< DateEnd > 2079 - 08 - 28 < / DateEnd >")
    file.write("< AdStatus > TurboSale < / AdStatus >")
    file.write("< AllowEmail > Да < / AllowEmail >")
    file.write("< ManagerName > Иван Петров - Водкин < / ManagerName >")
    file.write("< ContactPhone > +7 916 683 - 78 - 22 < / ContactPhone >")
    file.write(" < Address > Владимирская область, г.Владимир, ул.Гагарина, 1 < / Address >")
    file.write("< Category > Одежда, обувь, аксессуары < / Category >")
    file.write("< GoodsType > Женская одежда < / GoodsType >")
    file.write("< Condition > Новое < / Condition >")
    file.write("< AdType > Товар приобретен напродажу < / AdType >")
    file.write("< Apparel > Платья и юбки < / Apparel >")
    file.write("< Size > S < / Size >")
    file.write("< Title > Прекрасное платье < / Title >")
    file.write("< Description > <![CDATA[ < p > Лёгкая и изящная юбка, не сковывает движения откроет ваши стройные гибкие ноги.На сцене такая юбка смотрится невероятно красиво и прелестно, она словно выступает неотъемлемым элементом происходящего там действия.Идеально подходит для вечера, корпоратива или же для повседневной жизни. < / p > < p > Сделана из тонких полупрозрачных тканей: < / p >< ul >< li > шифона < / li > < li > фатина < / li >< li > сетки < / li >< / ul >]] > < / Description >")
    file.write("< Price > 25300 < / Price >")
    file.write("< Images >< Image url = \"http://img.test.ru/8F7B-4A4F3A0F2BA1.jpg\" / >< Image url = \"http://img.test.ru/8F7B-4A4F3A0F2XA3.jpg\" / >< / Images >")
    file.write("< VideoURL > http: // www.youtube.com / watch?v = YKmDXNrDdBI < / VideoURL >")
    file.write("< / Ad >< / Ads >")

    file.close()


def digital_product(request: object, token: str) -> Union[FileResponse, HttpResponseNotFound]:
    """Return the direct download link to content if given token is still valid."""


    qs = DigitalContentUrl.objects.prefetch_related("line__order__user")
    content_url = get_object_or_404(qs, token=token)  # type: DigitalContentUrl
    if not digital_content_url_is_valid(content_url):
        return HttpResponseNotFound("Url is not valid anymore")

    digital_content = content_url.content
    digital_content.content_file.open()
    opened_file = digital_content.content_file.file
    filename = os.path.basename(digital_content.content_file.name)
    file_expr = 'filename="{}"'.format(filename)

    content_type = mimetypes.guess_type(str(filename))[0]
    response = FileResponse(opened_file)
    response["Content-Length"] = digital_content.content_file.size

    response["Content-Type"] = str(content_type)
    response["Content-Disposition"] = "attachment; {}".format(file_expr)

    increment_download_count(content_url)
    return response
