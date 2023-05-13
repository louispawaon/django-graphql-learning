import graphene
from graphene_django import DjangoObjectType
from books.models import Book, Publisher, Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class Query(graphene.ObjectType):
    books = graphene.List(BookType)
    publishers = graphene.List(PublisherType)
    authors = graphene.List(AuthorType)

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_publishers(self, info):
        return Publisher.objects.all()

    def resolve_authors(self, info):
        return Author.objects.all()


schema = graphene.Schema(query=Query)
