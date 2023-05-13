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


class CreatePublisherMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        city = graphene.String(required=True)
        stateProvince = graphene.String(required=True)
        country = graphene.String(required=True)
        website = graphene.String(
            required=True
        )  # Can be modified into custom Scalar Type

    publisher = graphene.Field(PublisherType)

    def mutate(self, info, name, address, city, stateProvince, country, website):
        publisher = Publisher.objects.create(
            name=name,
            address=address,
            city=city,
            state_province=stateProvince,
            country=country,
            website=website,
        )

        # You can insert code logic if required (e.g. handling duplicate entries)

        publisher.save()

        return CreatePublisherMutation(publisher=publisher)


class CreateAuthorMutation(graphene.Mutation):
    class Arguments:
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        email = graphene.String(
            required=True
        )  # Can be modified into custom Scalar Type

    author = graphene.Field(AuthorType)

    def mutate(self, info, firstName, lastName, email):
        author = Author.objects.create(
            first_name=firstName, last_name=lastName, email=email
        )

        # You can insert code logic if required (e.g. handling duplicate entries)

        author.save()
        return CreateAuthorMutation(author=author)


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        authorID = graphene.Int(required=True)
        publisherID = graphene.Int(required=True)
        publicationDate = graphene.Date(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, authorID, publisherID, publicationDate):
        author = Author.objects.get(pk=authorID)
        publisher = Publisher.objects.get(pk=publisherID)
        book = Book.objects.create(
            title=title,
            publication_date=publicationDate,
        )
        book.authors.add(author)
        book.publisher = publisher

        # You can insert code logic if required (e.g. handling duplicate entries)

        book.save()
        return CreateBookMutation(book=book)


class Mutation(graphene.ObjectType):
    createPublisher = CreatePublisherMutation.Field()
    createAuthor = CreateAuthorMutation.Field()
    createBook = CreateBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
