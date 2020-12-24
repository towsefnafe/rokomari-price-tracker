from django.shortcuts import render, redirect
from .models import Book
import requests
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
	books = Book.objects.all()
	context = {
		'books': books,
	}
	return render(request, 'home.html', context)

def add(request):
	if request.method == 'POST':
		link = request.POST.get('link')
		b = Book(link=link)
		b.save()
		return redirect('home')
	return render(request, 'add.html')

def delete(request, id):
	book = Book.objects.get(id=id)
	if request.method == 'POST':
		book.delete()
		return redirect('home')
	r = requests.get(book.link)
	soup = BeautifulSoup(r.text, 'html.parser')
	book_name = soup.select('p.book-name')[0].text
	author_name = soup.select('p.author-name a')[0].text
	context = {
		'book': book,
		'book_name': book_name,
		'author_name': author_name,
	}
	return render(request, 'delete.html', context)

def details(request, id):
	book = Book.objects.get(id=id)
	r = requests.get(book.link)
	soup = BeautifulSoup(r.text, 'html.parser')
	book_name = soup.select('p.book-name')[0].text
	author_name = soup.select('p.author-name a')[0].text
	s_price = soup.select('span.sell-price')[0].text
	try:
		o_price = soup.select('strike.original-price')[0].text
	except:
		o_price = s_price
	if s_price == o_price:
		s_price = 'This book has no discount.'
	context = {
		'book': book,
		'book_name': book_name,
		'author_name': author_name,
		's_price': s_price,
		'o_price': o_price
	}
	return render(request, 'details.html', context)