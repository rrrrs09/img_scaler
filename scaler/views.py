from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import UploadedImage
from .forms import UploadForm, ResizeForm
from .utils import resize, get_image_from_url


def index(request):
    return render(
        request,
        'scaler/index.html',
        {'images': UploadedImage.objects.all()}
    )


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            image = form.cleaned_data.get('image')
            if url:
                try:
                    downloaded_img, img_name = get_image_from_url(url)
                except ValidationError as error:
                    form.add_error('url', error)
                else:
                    image = UploadedImage()
                    image.img.save(img_name, downloaded_img, save=True)
                    return redirect('detail', pk=image.pk)
            else:
                image = UploadedImage(img=request.FILES['image'])
                image.save()
                return redirect('detail', pk=image.pk)
    else:
        form = UploadForm()
    return render(request, 'scaler/upload.html', {'form': form})


def detail(request, pk):
    image = get_object_or_404(UploadedImage, pk=pk)
    if request.method == 'POST':
        form = ResizeForm(request.POST, image=image)
        if form.is_valid():
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']

            image_ratio = round(image.img.width / image.img.height, 2)
            if width and not height:
                height = int(width / image_ratio)

            elif height and not width:
                width = int(height * image_ratio)

            resized_img = resize(image.img, width, height)

            name = image.img.name.split('.')
            img_name, img_format = name[0], name[1]
            img_name = img_name.replace('_{}x{}'.format(image.img.width, image.img.height), '')

            new_name = f'{img_name}_{width}x{height}.{img_format}'
            image = UploadedImage()
            image.img.save(new_name, resized_img, save=True)
    else:
        form = ResizeForm(
            {'width': image.img.width,
            'height': image.img.height},
            image=image
        )
    return render(request, 'scaler/detail.html', {'image': image, 'form': form})
