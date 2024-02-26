import graphene
from graphene import ObjectType
from graphene_django.types import DjangoObjectType

from web.models import User, TaskList


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TaskListType(DjangoObjectType):
    class Meta:
        model = TaskList


class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    task_list = graphene.Field(TaskListType, id=graphene.Int())
    users = graphene.List(UserType)
    task_lists = graphene.List(TaskListType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(pk=id)
        return None

    def resolve_task_list(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return TaskList.objects.get(pk=id)
        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_task_lists(self, info, **kwargs):
        return TaskList.objects.all()


class TaskListInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    created_user = graphene.ID()


class CreateTaskList(graphene.Mutation):
    class Arguments:
        input = TaskListInput(required=True)

    ok = graphene.Boolean()
    task_list = graphene.Field(TaskListType)

    @staticmethod
    def mutate(root, info, input=None):
        print(User.objects.get(id=input.created_user))
        ok = True
        task_list_instance = TaskList(
            title=input.title,
            created_user=User.objects.get(id=input.created_user)
        )
        task_list_instance.save()
        return CreateTaskList(ok=ok, task_list=task_list_instance)


class Mutation(graphene.ObjectType):
    create_task_list = CreateTaskList.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
