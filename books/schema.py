import graphene
import re
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from books.models import Book, Publisher, Author

"""
Custom Scalar Types 
"""


# Website Custom Scalar Type
class Website(graphene.Scalar):
    website_pattern = re.compile(
        r"^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
    )

    @staticmethod
    def serialize(
        value,
    ):  # Converting the Scalar Value to a Serialized Value to be sent in network
        if not Website.is_valid(value):
            raise ValueError(f"Invalid Website URL: {value}")
        return value

    @staticmethod
    def parse_literal(
        node,
    ):  # Converting the literal value from GraphQL query to Python object
        if not Website.is_valid(node.value):
            raise GraphQLError(f"Invalid Website URL: {node.value}")
        return node.value

    @staticmethod
    def parse_value(
        value,
    ):  # Converting runtime value to scalar type expected by the schema
        if not Website.is_valid(value):
            raise ValueError(f"Invalid Webiste URL: {value}")
        return value

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and Website.website_pattern.match(value)


# Email Custom Scalar Type
class Email(graphene.Scalar):
    email_pattern = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )

    @staticmethod
    def serialize(
        value,
    ):  # Converting the Scalar Value to a Serialized Value to be sent in network
        if not Email.is_valid(value):
            raise ValueError(f"Invalid Email Address: {value}")
        return value

    @staticmethod
    def parse_literal(
        node,
    ):  # Converting the literal value from GraphQL query to Python object
        if not Email.is_valid(node.value):
            raise GraphQLError(f"Invalid Email Address: {node.value}")
        return node.value

    @staticmethod
    def parse_value(
        value,
    ):  # Converting runtime value to scalar type expected by the schema
        if not Email.is_valid(value):
            raise ValueError(f"Invalid Email Address: {value}")
        return value

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and Email.email_pattern.match(value)


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


"""
Publisher CRUD Methods
"""


class CreatePublisherMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        city = graphene.String(required=True)
        stateProvince = graphene.String(required=True)
        country = graphene.String(required=True)
        website = Website(required=True)

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


class UpdatePublisherMutation(graphene.Mutation):
    publisherID = graphene.ID(required=True)
    name = graphene.String(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    stateProvince = graphene.String(required=True)
    country = graphene.String(required=True)
    website = Website(required=True)

    publisher = graphene.Field(PublisherType)

    def mutate(
        self,
        info,
        publisherID,
        name,
        address,
        city,
        stateProvince,
        country,
        website,
    ):
        try:
            publisher = Publisher.objects.get(
                pk=publisherID
            )  # Check if Publisher Exists
        except Publisher.DoesNotExist:
            raise GraphQLError(f"Book with id {publisherID} does not exist")

        if name:
            publisher.name = name
        if address:
            publisher.address = address
        if city:
            publisher.city = city
        if stateProvince:
            publisher.state_province = stateProvince
        if country:
            publisher.country = country
        if website:
            publisher.website = website

        publisher.save()
        return UpdatePublisherMutation(publisher=publisher)


class DeletePublisherMutation(graphene.Mutation):
    class Arguments:
        publisherID = graphene.ID(required=True)

    publisherID = graphene.ID()

    def mutate(self, info, publisherID):
        try:
            publisher = Publisher.objects.get(
                pk=publisherID
            )  # Check if Publisher Exists
        except Publisher.DoesNotExist:
            raise GraphQLError(f"Publisher with id {publisherID} does not exist")

        publisher.delete()
        return DeletePublisherMutation(publisherID=publisherID)


"""
Author CRUD Methods
"""


class CreateAuthorMutation(graphene.Mutation):
    class Arguments:
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        email = Email(required=True)

    author = graphene.Field(AuthorType)

    def mutate(self, info, firstName, lastName, email):
        author = Author.objects.create(
            first_name=firstName, last_name=lastName, email=email
        )

        # You can insert code logic if required (e.g. handling duplicate entries)

        author.save()
        return CreateAuthorMutation(author=author)


class UpdateAuthorMutation(graphene.Mutation):
    authorID = graphene.ID(required=True)
    firstName = graphene.String(required=True)
    lastName = graphene.String(required=True)
    email = Email(required=True)

    author = graphene.Field(PublisherType)

    def mutate(self, info, authorID, firstName, lastName, email):
        try:
            author = Author.objects.get(pk=authorID)  # Check if Publisher Exists
        except Author.DoesNotExist:
            raise GraphQLError(f"Book with id {authorID} does not exist")

        if firstName:
            author.first_name = firstName
        if lastName:
            author.last_name = lastName
        if email:
            author.email = email

        author.save()
        return UpdateAuthorMutation(author=author)


class DeleteAuthorMutation(graphene.Mutation):
    class Arguments:
        authorID = graphene.ID(required=True)

    authorID = graphene.ID()

    def mutate(self, info, authorID):
        try:
            author = Author.objects.get(pk=authorID)  # Check if Publisher Exists
        except Publisher.DoesNotExist:
            raise GraphQLError(f"Author with id {authorID} does not exist")

        author.delete()
        return DeleteAuthorMutation(authorID=authorID)


"""
Book CRUD Methods
"""


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


class UpdateBookMutation(graphene.Mutation):
    bookID = graphene.ID(required=True)
    title = graphene.String(required=True)
    authorID = graphene.Int(required=True)
    publisherID = graphene.Int(required=True)
    publicationDate = graphene.Date(required=True)

    book = graphene.Field(PublisherType)

    def mutate(self, info, bookID, title, authorID, publisherID, publicationDate):
        try:
            book = Book.objects.get(pk=bookID)  # Check if Publisher Exists
        except Book.DoesNotExist:
            raise GraphQLError(f"Book with id {bookID} does not exist")

        if title:
            book.title = title
        if authorID:
            try:
                author = Author.objects.get(pk=authorID)
            except Book.DoesNotExist:
                raise GraphQLError(
                    f"Book with author that has id {authorID} does not exist"
                )
            book.authors = [author]
        if publisherID:
            try:
                publisher = Publisher.objects.get(pk=publisherID)
            except Publisher.DoesNotExist:
                raise GraphQLError(
                    f"Book with publisher that has id {publisherID} does not exist"
                )
        if publicationDate:
            book.publication_date = (
                publicationDate  # Can be checked if date given is valid
            )

        book.save()
        return UpdateBookMutation(book=book)


class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        bookID = graphene.ID(required=True)

    bookID = graphene.ID()

    def mutate(self, info, bookID):
        try:
            book = Book.objects.get(pk=bookID)  # Check if Publisher Exists
        except Publisher.DoesNotExist:
            raise GraphQLError(f"book with id {bookID} does not exist")

        book.delete()
        return DeleteBookMutation(bookID=bookID)


# Mutation Class
class Mutation(graphene.ObjectType):
    createPublisher = CreatePublisherMutation.Field()
    createAuthor = CreateAuthorMutation.Field()
    createBook = CreateBookMutation.Field()
    updatePublisher = UpdatePublisherMutation.Field()
    updateAuthor = UpdateAuthorMutation.Field()
    updateBook = UpdateBookMutation.Field()
    deletePublisher = DeletePublisherMutation.Field()
    deleteAuthor = DeleteAuthorMutation.Field()
    deletBook = DeleteBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
