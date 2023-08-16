from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm
from .genetic import genetic_algorithm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.method == 'POST':
        jumlah_barang = int(request.POST.get('jumlah_barang', 0))
        batas_bobot = int(request.POST.get('batas_bobot', 0))
        jenis_seleksi = request.POST.get('seleksi', '')
        
        # Validasi jika tombol "Submit" ditekan dan nilai 'jumlah_barang' atau 'batas_bobot' tidak valid
        #if jumlah_barang <= 0 or batas_bobot <= 0:
         #   return HttpResponse("Jumlah barang dan batas bobot harus lebih dari 0.")
        
        #else:
        # Panggil fungsi genetic_algorithm dengan meneruskan nilai jumlah_barang dan batas_bobot
        #result = genetic_algorithm(jumlah_barang, batas_bobot, jenis_seleksi)
        best_result = genetic_algorithm(jumlah_barang, batas_bobot, jenis_seleksi)

        # Buat context dictionary dengan data yang ingin dikirimkan ke template
        
        context = {
            'jumlah_barang': jumlah_barang,
            'batas_bobot': batas_bobot,
            'jenis_seleksi': jenis_seleksi,
            'best_results': best_result,}

        # Modifikasi render untuk mengirimkan hasil algoritma genetika ke template
        #context = {
            #'result': result,
        #}
        return render(request, 'dashboard/index.html', context)

    return render(request, 'dashboard/index.html')

def staff(request):
    workers = User.objects.all()
    context={
        'workers':workers
    }
    return render (request, 'dashboard/staff.html',context)
def product(request):
    items = Product.objects.all()
    #items = Product.objects.raw('SELECT * FROM dashboard_product')
    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context={
        'items': items,
        'form': form,
    }
    return render (request, 'dashboard/product.html', context)

def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context={
        'form': form,

    }
    return render(request, 'dashboard/product_update.html', context)


def order(request):
    return render (request, 'dashboard/order.html')