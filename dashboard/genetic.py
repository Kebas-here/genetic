from django.shortcuts import render, HttpResponse
import random
from .models import Product
# Fungsi view untuk halaman index
def index(request):
    if request.method == 'POST':
        jumlah_barang = int(request.POST.get('jumlah_barang', 0))  # Mendapatkan nilai dari input 'jumlah_barang'
        batas_bobot = int(request.POST.get('batas_bobot', 0))  # Mendapatkan nilai dari input 'batas_bobot'
        jenis_seleksi = request.POST.get('seleksi','')
        if jumlah_barang <= 0 or batas_bobot <= 0:
            return HttpResponse("Jumlah barang dan batas bobot harus lebih dari 0.")
        # Panggil fungsi genetic_algorithm dengan meneruskan nilai jumlah_barang dan batas_bobot
        result = genetic_algorithm(jumlah_barang, batas_bobot, jenis_seleksi)
        # Lakukan proses lain sesuai kebutuhan
        return HttpResponse(result)
    return render(request, 'dashboard/index.html')  # Render halaman index dengan form

# Fungsi genetic_algorithm dengan parameter 'jumlah_barang' dan 'batas_bobot'

# Inisialisasi variabel knapsack
capacity = 0  # Inisialisasi awal capacity
population_size = 20
generations = 30
products = Product.objects.all()
product_names = [str(product.nama for product in products)]
prices = [int(product.hargam / 1000) for product in products]
values = [int(product.harga / 1000) for product in products]
weights = prices
# Inisialisasi populasi
def create_individual(jumlah_barang):

    while True:
        individual = [random.randint(0, 1) for _ in range(len(weights))]
        total = sum(individual)
        
        if total <= jumlah_barang:
            return individual

# Evaluasi individu
def fitness(individual):
    weight = sum(individual[i] * weights[i] for i in range(len(weights)))
    if weight > capacity:
        return 0
    return sum(individual[i] * values[i] for i in range(len(values)))

def selection_elitism(population):
    sorted_population = sorted(population, key=lambda individual: fitness(individual), reverse=True)
    elite = sorted_population[:2]  # Memilih dua individu terbaik sebagai elit
    return elite

# Seleksi (roulette wheel selection)
def selection(population):
    fitness_scores = [fitness(individual) for individual in population]
    total_fitness = sum(fitness_scores)
    if total_fitness == 0:
        return random.choices(population, k=2)
    return random.choices(population, weights=fitness_scores, k=2)

def selection_tournament(population, tournament_size):
    tournament_size = 3  # Ukuran turnamen
    selected_parents = []
    for _ in range(len(population)):
        tournament_candidates = random.sample(population, tournament_size)
        winner = max(tournament_candidates, key=lambda individual: fitness(individual))
        selected_parents.append(winner)
    return selected_parents
# Crossover
def crossover(parents, jumlah_barang):
    max_attempts = 10
    for _ in range(max_attempts):
        crossover_point = random.randint(1, len(weights) - 1)
        child1 = parents[0][:crossover_point] + parents[1][crossover_point:]
        child2 = parents[1][:crossover_point] + parents[0][crossover_point:]

        if sum(child1) <= jumlah_barang and sum(child2) <= jumlah_barang:
            return child1, child2

    # Jika setelah beberapa percobaan crossover tidak berhasil, kembalikan salah satu orangtua
    return parents[0], parents[1]

# Mutasi
def mutation(individual):
    index = random.randint(0, len(weights) - 1)
    individual[index] = 1 - individual[index]
    return individual

# Algoritma genetika
def genetic_algorithm(jumlah_barang, batas_bobot, jenis_seleksi):
    global capacity  # Mendeklarasikan bahwa kita akan menggunakan variabel capacity global
    capacity = batas_bobot  # Mengubah nilai capacity menjadi nilai batas_bobot
    num_selected_items = jumlah_barang
    if num_selected_items > len(weights):
        return "Jumlah barang yang ingin dipilih melebihi jumlah barang yang ada."
    
def genetic_algorithm(jumlah_barang, batas_bobot, jenis_seleksi):
    global capacity
    capacity = batas_bobot
    num_selected_items = jumlah_barang
    if num_selected_items > len(weights):
        return "Jumlah barang yang ingin dipilih melebihi jumlah barang yang ada."

    best_result = []  # Variabel untuk menyimpan hasil 5 individu terpilih
    selected_individuals = []
    best_chromosomes_per_generation = []  # Menyimpan kromosom terbaik dari setiap generasi
    for no in range(population_size):
        population = create_population(jumlah_barang)
        selection_type = jenis_seleksi
        if selection_type == "tournament":
            selection_type = "tournament"
        for generation in range(generations):
            new_population = []
            for _ in range(population_size // 2):
                if selection_type == "elitism":
                    parents = selection_elitism(population)
                elif selection_type == "tournament":
                    parents = selection_tournament(population, tournament_size=3)
                else:
                    parents = selection(population)
                children = crossover(parents, jumlah_barang)
                child1 = mutation(children[0])
                child2 = mutation(children[1])
                new_population.append(child1)
                new_population.append(child2)
            population = new_population
            best_individual = max(population, key=fitness)
            selected_indexes = [i for i, chrom in enumerate(best_individual) if chrom > 0]
            selected_weights = [weights[i] for i in selected_indexes]
            if selection_type == "roulette wheel":
                while len(selected_indexes) == 0 or sum(selected_weights) == 0:
                    best_individual = random.choice(population)
                    selected_indexes = [i for i, chrom in enumerate(best_individual) if chrom > 0]
                    selected_weights = [weights[i] for i in selected_indexes]
            selected_individuals.append((selected_indexes, selected_weights))

        best_chromosome = max(population, key=fitness)
        best_chromosomes_per_generation.append(best_chromosome)
        # Mengambil 5 kromosom terbaik dari setiap generasi berdasarkan fitness score
        best_result = sorted(best_chromosomes_per_generation, key=fitness, reverse=True)[:5]

        # Mengambil informasi individu terpilih dari 5 kromosom terbaik
        selected_results = []
        for chromosome in best_result:
            selected_indexes = [i for i, chrom in enumerate(chromosome) if chrom > 0]
            selected_indexes_with_offset = [index + 1 for index in selected_indexes]
            selected_weights = [weights[i] for i in selected_indexes]
            selected_values = [values[i] for i in selected_indexes]
            total_weight = sum(selected_weights)
            total_value = sum(selected_values)
            selected_product_names = [products[i - 1].nama for i in selected_indexes_with_offset]
            selected_results.append({
                
                'produk ke ' : selected_indexes_with_offset,
                'Modal ': total_weight,
                'Harga Jual': total_value, 
                'Nama Produk' : selected_product_names,
            })

    return selected_results
# Panggil fungsi create_population di dalam fungsi genetic_algorithm
def create_population(jumlah_barang):
    return [create_individual(jumlah_barang) for _ in range(population_size)]

