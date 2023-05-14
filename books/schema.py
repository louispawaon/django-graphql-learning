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
        r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
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


"""
Custom Error Messages
"""


class BookAlreadyExistsError(GraphQLError):
    message = "A book with the same title already exists in the database."

    def __init__(self, message):
        super().__init__(message)


class AuthorAlreadyExistsError(GraphQLError):
    message = "An author with the same name already exists in the database."

    def __init__(self, message):
        super().__init__(message)


class PublisherAlreadyExistsError(GraphQLError):
    message = "A publisher with the same name already exists in the database."

    def __init__(self, message):
        super().__init__(message)


"""
DjangoObjectTypes
"""


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

    @classmethod
    def filter_author(cls, queryset, info, **kwargs):
        firstName = kwargs.get("firstName")
        lastName = kwargs.get("lastName")

        if firstName:
            queryset = queryset.filter(first_name__icontains=firstName)
        if lastName:
            queryset = queryset.filter(last_name__icontains=lastName)

        return queryset


class Query(graphene.ObjectType):
    books = graphene.List(BookType, search=graphene.String())
    publishers = graphene.List(PublisherType, search=graphene.String())
    authors = graphene.List(AuthorType, search=graphene.String())

    def resolve_books(self, info, search=None):
        if search:
            return Book.objects.filter(title__icontains=search)
        else:
            return Book.objects.all()

    def resolve_publishers(self, info, search=None):
        if search:
            return Book.objects.filter(name__icontrains=search)
        else:
            return Publisher.objects.all()

    def resolve_authors(self, info, search=None, **kwargs):
        queryset = Author.objects.all()
        if search:
            queryset = AuthorType.filter_author(queryset, search)
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
        # You can insert code logic if required (e.g. handling duplicate entries)

        publisher_exists = Publisher.objects.filter(name=name).first()

        if publisher_exists:
            raise PublisherAlreadyExistsError(
                message="A publisher with the same name already exists in the database."
            )

        publisher = Publisher.objects.create(
            name=name,
            address=address,
            city=city,
            state_province=stateProvince,
            country=country,
            website=website,
        )

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
        # You can insert code logic if required (e.g. handling duplicate entries)

        author_exists = Author.objects.filter(
            first_name=firstName, last_name=lastName
        ).first()

        if author_exists:
            raise AuthorAlreadyExistsError(
                message="An author with the same name already exists in the database."
            )

        author = Author.objects.create(
            first_name=firstName, last_name=lastName, email=email
        )

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
        # You can insert code logic if required (e.g. handling duplicate entries)

        book_exists = Book.objects.filter(title=title).first()

        if book_exists:
            raise BookAlreadyExistsError(
                message="A book with the same title already exists in the database."
            )

        author = Author.objects.get(pk=authorID)
        publisher = Publisher.objects.get(pk=publisherID)
        book = Book.objects.create(
            title=title,
            publication_date=publicationDate,
        )
        book.authors.add(author)
        book.publisher = publisher

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
