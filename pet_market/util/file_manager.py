import os
from pet_market.models import ItemImages


def upload_item_image(item, image_files):

    base_dir = os.getcwd()
    image_model = ItemImages.objects.get_or_create(item=item)[0]
    count = image_model.count
    if count + len(image_files) > 5:
        return False

    for image in image_files:
        new_image_filename = 'product%d_%d.jpg' % (item.id, count+1)
        new_image_address = os.path.join('item_images', new_image_filename)
        full_image_address = os.path.join(base_dir, 'media', new_image_address)
        with open(full_image_address, 'wb+') as destination_file:
            try:
                for chunks in image.chunks():
                    destination_file.write(chunks)
            except:
                print('error saving image')
                return False

        count += 1
        if count == 1:
            image_model.image_1 = new_image_address
        elif count == 2:
            image_model.image_2 = new_image_address
        elif count == 3:
            image_model.image_3 = new_image_address
        elif count == 4:
            image_model.image_4 = new_image_address
        elif count == 5:
            image_model.image_5 = new_image_address

        image_model.count = count
        image_model.save()

    return True
