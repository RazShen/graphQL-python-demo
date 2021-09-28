import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required=False)


class Query(graphene.ObjectType):
    is_staff = graphene.Boolean()
    is_member = graphene.Boolean()
    users = graphene.List(User, first=graphene.Int())

    def resolve_is_staff(self, info):
        return True

    def resolve_is_member(self, info):
        return False

    def resolve_users(self, info, first):
        return [
                   User(username='Alice', last_login=datetime.now()),
                   User(username='Raz', last_login=datetime.now()),
                   User(username='Maya', last_login=datetime.now()),
                   User(username='Kyle', last_login=datetime.now())
               ][:first]


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        if info.context.get('is_vip'):
            username=username.upper()
        user = User(username=username)

        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

# result = schema.execute(
#     '''
#     {
#         isStaff
#         isMember
#     }
#     '''
# )
# result = schema.execute(
#     '''
#     {
#         users(first : 2) {
#             username
#         }
#     }
#     '''
# )
result = schema.execute(
    '''
    mutation createUser($username: String) {
        createUser(username: $username) {
            user {
                username
            }
        }
    }   
    ''',
    variable_values={'username': 'Raz'},
    context={'is_vip': 'True'}
)

items = dict(result.data.items())
print(json.dumps(items, indent=4))
