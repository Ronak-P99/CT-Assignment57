import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Bakery as BakeryModel, db
from sqlalchemy.orm import Session

class Bakery(SQLAlchemyObjectType):
    class Meta:
        model = BakeryModel # This is mapping to the Bakery model in our models.py

class Query(graphene.ObjectType):
    bakeries = graphene.List(Bakery)

    def resolve_bakeries(self, info): # Resolver
        return db.session.execute(db.select(BakeryModel)).scalars()
    
class AddBakery(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        category = graphene.String(required=True)
        price = graphene.Float(required=True)


    bakery = graphene.Field(Bakery)

    def mutate(self, info, name, quantity, category, price):
        with Session(db.engine) as session:
            with session.begin():
                bakery = BakeryModel(name=name, quantity=quantity, category=category, price=price)
                session.add(bakery)
            
            session.refresh(bakery)
            return AddBakery(bakery=bakery)
        
class UpdateBakery(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        category = graphene.String(required=True)
        price = graphene.Float(required=True)

    bakery = graphene.Field(Bakery)

    def mutate(self, info, id, name, quantity, category, price):
        with Session(db.engine) as session:
            with session.begin():
                bakery = session.execute(db.select(BakeryModel).where(BakeryModel.id == id)).scalars().first()
                if bakery:
                    bakery.name = name
                    bakery.quantity = quantity
                    bakery.category = category
                    bakery.price = price
                else:
                    return None
            session.refresh(bakery)
            return UpdateBakery(bakery=bakery)

    
class DeleteBakery(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    bakery = graphene.Field(Bakery)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                bakery = session.execute(db.select(BakeryModel).where(BakeryModel.id == id)).scalars().first()
                if bakery:
                   session.delete(bakery)
                else:
                    return None
            session.refresh(bakery)
            return DeleteBakery(bakery=bakery)

            
    
class Mutation(graphene.ObjectType):
    create_bakery = AddBakery.Field()
    update_bakery = UpdateBakery.Field()
    delete_bakery = DeleteBakery.Field()