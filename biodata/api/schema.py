import graphene
from graphene_django import DjangoObjectType

from biodata.api import models as m
from biodata.api import queries
from biodata.api import mutations


class Query(
    queries.Query,
    graphene.ObjectType
):
    pass


class Mutation(
#    mt.CreateStudyMutation,
    mutations.Mutation,
#    mt.CreateBiospecimenMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
