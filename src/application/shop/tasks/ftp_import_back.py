import xml.etree.ElementTree as XMLTree

from django.core.files import File
from django.db import transaction
from django.utils.text import slugify

from celery.task import task
from ftplib import FTP, error_perm
from preferences.utils import get_setting
from os import unlink, path
from unidecode import unidecode
from django.forms.models import model_to_dict


@task(name='import_catalog_from_ftp')
def import_catalog_from_ftp():

    from application.shop.models import Category, Good, GoodImage, Shop, PriceInShop

    for i in Good.objects.all():
        i.save()

    goods = set(Good.objects.values_list('vendor_code', flat=True))

    ftp_server = get_setting('shop_importftpserver')
    ftp_user = get_setting('shop_importftpuser')
    ftp_password = get_setting('shop_importftppassword')
    # ftp_file = get_setting('shop_importgoodsfile')
    ftp_images_path = get_setting('shop_importimagespath')
    ftp_desc_path = get_setting('shop_importdescriptionspath')
    ftp = FTP(ftp_server)
    ftp.login(ftp_user, ftp_password)

    shops = Shop.objects.all()

    for shop in shops:
        temp_file_name_goods = "".join([
            "/tmp/",
            shop.goods_file.rsplit("/", 1)[1],
        ])

        with open(temp_file_name_goods, 'wb') as f:
            try:
                ftp.retrbinary('RETR ' + shop.goods_file, f.write)
            except error_perm:
                print(error_perm)
                continue

        if not path.exists(temp_file_name_goods):
            print("File not found: {}".format(shop.goods_file))
            continue

        default_shop = shop.is_default_shop()
        is_first_import = True
        f = open(temp_file_name_goods, 'r')

        with transaction.atomic():

            try:
                # delete all prices for this shop before upload
                # of new data.
                PriceInShop.objects.filter(shop=shop).delete()
                for line in f.readlines():
                    try:
                        a = line.split(';')

                        name = a[0].strip()
                        vendor_code = a[1].strip()
                        cat_1_name = a[2].strip()
                        cat_2_name = a[3].strip()
                        cat_3_name = a[4].strip()
                        is_sale = not (a[5] == 'Ложь')
                        is_new = not (a[6] == 'Ложь')
                        is_hit = not (a[7] == 'Ложь')
                        price = round(float(a[8].strip().replace(',', '.')))
                        price_card = round(float(a[9].strip().replace(',', '.')))
                        count = a[10].strip()
                        title = a[11].strip()
                        is_order = (count == '0' and a[12].strip() == '1')

                        # CATEGORIES

                        try:
                            category_1 = Category.objects.get(name__iexact=cat_1_name, parent__isnull=True)
                        except Category.DoesNotExist:
                            slug = slugify(unidecode(cat_1_name))
                            category_1 = Category(name=cat_1_name, slug=slug)
                            category_1.save()

                        category = category_1

                        if cat_2_name:
                            try:
                                category_2 = Category.objects.get(name__iexact=cat_2_name, parent=category_1)
                            except Category.DoesNotExist:
                                slug = slugify(unidecode(cat_2_name))
                                category_2 = Category(name=cat_2_name, slug=slug, parent=category_1)
                                category_2.save()
                            category = category_2
                        else:
                            category_2 = None

                        if cat_3_name and category_2:
                            try:
                                category_3 = Category.objects.get(name__iexact=cat_3_name, parent=category_2)
                            except Category.DoesNotExist:
                                slug = slugify(unidecode(cat_3_name))
                                category_3 = Category(name=cat_3_name, slug=slug, parent=category_2)
                                category_3.save()

                            category = category_3

                        # GOODS
                        if not vendor_code:
                            continue

                        try:
                            good = Good.objects.get(vendor_code=vendor_code)
                        except Good.DoesNotExist:
                            good = Good()
                            good.vendor_code = vendor_code
                            good.slug = '%s-%s' % (slugify(unidecode(name)), vendor_code)

                        if is_first_import:
                            good.count = 0
                            is_first_import = False

                        goods.discard(vendor_code)

                        if default_shop:
                            if price:
                                good.price = price
                            if price_card:
                                good.price_card = price_card
                            good.is_order = is_order

                        good.category = category
                        good.name = name
                        good.is_sale = is_sale
                        good.is_new = is_new
                        good.is_hit = is_hit
                        good.title = title
                        good.save()

                        try:
                            price_in_shop = PriceInShop.objects.get(
                                shop=shop,
                                good=good,
                            )
                        except PriceInShop.DoesNotExist:
                            price_in_shop = PriceInShop.objects.create(
                                shop=shop,
                                good=good,
                            )

                        price_in_shop.price = price if price else 0
                        price_in_shop.price_card = price_card if price_card else 0
                        price_in_shop.count = count
                        price_in_shop.is_order = is_order
                        price_in_shop.is_sale = is_sale
                        price_in_shop.is_new = is_new
                        price_in_shop.is_hit = is_hit
                        price_in_shop.save()

                        good.update_count()
                    except Exception as e:
                        print("Exception in file {} in line {}: {}".format(f.name, line, e))

                print("Data imported {}.".format(f.name))
            except Exception as e:
                print("File {} contain next exception: {}".format(f.name, e))

        f.close()
        unlink(temp_file_name_goods)

    # Images
    ftp.cwd(ftp_images_path)
    img_files = ftp.nlst()
    for i in img_files:

        vendor_code = i.replace('.jpg', '')

        try:
            g = Good.objects.get(vendor_code=vendor_code)

            # Single image
            if '.jpg' in i:
                is_load_image = False
                if not g.image:
                    is_load_image = True
                else:
                    size_source = path.getsize(g.image.path)
                    size_ftp = ftp.size(i)
                    if size_source != size_ftp:
                        g.image.delete()
                        is_load_image = True
                if is_load_image:
                    temp_img_file_name = '/tmp/%s.jpg' % vendor_code
                    with open(temp_img_file_name, 'wb') as f:
                        ftp.retrbinary('RETR ' + i, f.write)
                    g.image.save(i, File(open(temp_img_file_name, 'rb')))
                    g.save()
                    unlink(temp_img_file_name)
            else:

                # Multiple images
                ftp.cwd(vendor_code)
                images_files = ftp.nlst()
                images_files = sorted(images_files)
                for j in images_files:
                    is_load_image = False
                    try:
                        gi = GoodImage.objects.get(name=j, good=g)
                        if not g.image:
                            is_load_image = True
                        else:
                            size_source = path.getsize(gi.image.path)
                            size_ftp = ftp.size(j)
                            if size_source != size_ftp:
                                gi.image.delete()
                                is_load_image = True
                    except GoodImage.DoesNotExist:
                        gi = GoodImage(name=j, good=g)
                        is_load_image = True
                    except Exception as e:
                        print('Exception occurs while updating image', str(e))
                        print('Deleting ', vendor_code, '_', j)
                        gi.delete()
                        gi = GoodImage(name=j, good=g)
                        is_load_image = True

                    if is_load_image:
                        temp_img_file_name = '/tmp/%s' % j
                        try:
                            with open(temp_img_file_name, 'wb') as f:
                                ftp.retrbinary('RETR ' + j, f.write)
                            gi.image.save('%s_%s' % (vendor_code, j), File(open(temp_img_file_name, 'rb')))
                            gi.save()
                            unlink(temp_img_file_name)
                        except Exception as e:
                            print('Error read file %s/%s' % (vendor_code, j))
                            print(str(e))


                ftp.cwd('..')

        except Good.DoesNotExist:
            pass
        except ValueError as va:
            print("Error with file: {}: {}".format(gi.image, va))
        except error_perm as ep:
            print("Error with file: {}: {}".format(gi.image, ep))



    # Descriptions
    ftp.cwd(ftp_desc_path)
    desc_files = ftp.nlst()

    for i in desc_files:
        vendor_code = i.replace('.txt', '')
        try:
            g = Good.objects.get(vendor_code=vendor_code)
            temp_file_name = '/tmp/%s' % i
            with open(temp_file_name, 'wb') as f:
                ftp.retrbinary('RETR ' + i, f.write)
            with open(temp_file_name, 'r') as f:
                data = f.read()
            g.content = data
            g.save()
            unlink(temp_file_name)
        except Good.DoesNotExist:
            pass

    # Quit
    ftp.quit()

    # Delete old goods
    Good.objects.filter(vendor_code__in=goods).delete()

    # Properties
    import_properties_from_ftp.delay()

    return 'Ok'


@task(name='import_properties_from_ftp')
def import_properties_from_ftp():

    from application.shop.models import Good, GoodProperty, Property, Brand

    ftp_server = get_setting('shop_importftpserver')
    ftp_user = get_setting('shop_importftpuser')
    ftp_password = get_setting('shop_importftppassword')
    ftp_file = get_setting('shop_importpropertiesfile')

    temp_file_name = '/tmp/properties mandarin.xml'

    ftp = FTP(ftp_server)
    ftp.login(ftp_user, ftp_password)

    with open(temp_file_name, 'wb') as f:
        ftp.retrbinary('RETR ' + ftp_file, f.write)

    with transaction.atomic():

        tree = XMLTree.parse(temp_file_name).getroot()

        for good_e in tree.findall('Артикул'):

            vendor_code = good_e.get('Ид')

            try:
                good = Good.objects.get(vendor_code=vendor_code)
            except Good.DoesNotExist:
                continue

            # Get properties
            props_f = []
            for prop_e in good_e.findall('Свойство'):

                name = prop_e.get('Ид')
                value = prop_e.text
                order = prop_e.get('Порядок')

                if value == 'Не определено':
                    continue

                if name != 'Производитель':
                    props_f.append({'name': name, 'value': value, 'order': order})
                else:
                    try:
                        brand = Brand.objects.get(slug=slugify(unidecode(value)))
                    except Brand.DoesNotExist:
                        brand = Brand(name=value, slug=slugify(unidecode(value)))
                        brand.save()
                    good.brand = brand
                    good.save()

            props_c = []
            gp = GoodProperty.objects.filter(good=good).prefetch_related('property')
            for i in gp:
                props_c.append({'i': i, 'name': i.property.name, 'value': i.value, 'exists': False,
                                'order': i.property.order})

            # Update properties
            for i_f in props_f:

                p = None
                pv = None
                for i_c in props_c:
                    if i_c['name'] == i_f['name']:
                        p = i_c
                    if i_c['name'] == i_f['name'] and i_c['value'] == i_f['value'] and \
                            str(i_c['order']) == str(i_f['order']):
                        i_c['exists'] = True
                        pv = i_c

                # New property
                if p is None:
                    p_obj, created = Property.objects.get_or_create(name=i_f['name'])
                    p_obj.order = i_f['order']
                    p_obj.save()
                    gpp = GoodProperty(property=p_obj, good=good, value=i_f['value'])
                    gpp.save()

                # Update property
                if pv is None and p is not None:
                    p['i'].value = i_f['value']
                    p['i'].save()
                    p['i'].property.order = i_f['order']
                    p['i'].property.save()
                    p['exists'] = True

            # Delete property
            for i_c in props_c:
                if not i_c['exists']:
                    i_c['i'].delete()

    unlink(temp_file_name)

    return 'Ok'
