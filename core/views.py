import requests
import graphene

from flask_graphql import GraphQLView

from graphene_sqlalchemy import (
  SQLAlchemyObjectType
)

from flask import request, session

from app import app

from core.models import (
  Car
)

def opa_allows(field):
  try:
    r = requests.post('http://localhost:8181/v1/data/graphql/allow', json={"input":{"user":session["user"], "field":field}})
    if r.json()["result"]:
      return True
    return False
  except Exception as e:
    print(e)
  return False

# SQLAlchemy Types
class CarObject(SQLAlchemyObjectType):
  class Meta:
    model = Car

  def resolve_price(self, info):
    if opa_allows('price'):
      return self.price

    return None

  def resolve_discountcode(self, info):
    if opa_allows('discount_code'):
      return self.discountcode

    return None


class Query(graphene.ObjectType):
  cars = graphene.List(CarObject)

  def resolve_cars(self, info):
    query = CarObject.get_query(info)
    return query.filter_by().order_by(Car.id.desc())


@app.route('/')
def index():
  return "<h1> GraphQL + OPA Demo </h1>"

@app.before_request
def set_user():
  user = request.headers.get("user", "guest")
  session['user'] = user

schema = graphene.Schema(query=Query)


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
  'graphql',
  schema=schema,
  batch=True
))

app.add_url_rule('/graphiql', view_func=GraphQLView.as_view(
  'graphiql',
  schema = schema,
  graphiql = True,
  batch=True
))