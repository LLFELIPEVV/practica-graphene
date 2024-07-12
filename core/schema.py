import graphene
from graphene_django import DjangoObjectType
from books.models import Book

# Define the BookType class that inherits from DjangoObjectType


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "created_at", "updated_at")


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        return CreateBookMutation(book=book)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
