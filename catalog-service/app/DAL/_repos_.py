from typing import Optional, List
from sqlalchemy.orm import Session

from common import CustomerSVCUtils
from ._models_ import CategoryModel, ProductModel, PurchaseModel
from ._dtos_ import CategoryCreateDTO, CategoryDTO, \
                    ProductCreateDTO, ProductDTO, \
                    PurchaseCreateDTO, PurchaseDTO, \
                    CustomerPurchaseCollectionDTO, CustomerPurchaseRecordDTO



class CategoryRepository():
    def __init__(self, session:Session) -> None:
        self.session = session
    
    def add(self, payload: CategoryCreateDTO) -> CategoryDTO:
        category = CategoryModel(**payload.model_dump())
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_all(self, skip:int=0, limit:int=10, ids:List[int]=None) -> Optional[List[CategoryDTO]]:
        if ids is None or len(ids)<1:
            categories = self.session.query(CategoryModel).offset(skip).limit(limit).all()
        else:
            categories = self.session.query(CategoryModel).filter(CategoryModel.id.in_(ids)).offset(skip).limit(limit).all()
        return categories

    def get(self, id) -> Optional[CategoryDTO]:
        category = self.session.query(CategoryModel).where(CategoryModel.id == id).first()
        if category is None:
            raise Exception(f"Category having ID: {id} does not exist")
        return category

    def modify(self, payload: CategoryDTO) -> CategoryDTO:
        category_proxy = self.session.query(CategoryModel).filter(CategoryModel.id == payload.id)
        if category_proxy.first() is None:
            raise Exception(f"Category having ID: {payload.id} does not exist")
        category_proxy.update(payload.model_dump(), synchronize_session=False)
        self.session.commit()
        return payload



class ProductRepository():
    def __init__(self, session:Session) -> None:
        self.session = session
    
    def add(self, payload: ProductCreateDTO, id:int = None) -> ProductDTO:
        payload.tags = ",".join([t.strip() for t in payload.tags])
        product = ProductModel(**payload.model_dump())

        if id is not None: product.id = id
        
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        dto = ProductDTO(title=product.title, category_id=product.category_id, description=product.description, tags=product.tags.split(','), id=product.id)
        return dto

    def get_all(self, skip:int=0, limit:int=10, ids:List[int]=None) -> Optional[List[ProductDTO]]:
        if ids is None or len(ids)<1:
            products = self.session.query(ProductModel).offset(skip).limit(limit).all()
        else:
            products = self.session.query(ProductModel).filter(ProductModel.id.in_(ids)).offset(skip).limit(limit).all()
        
        dtos:List[ProductDTO] = []
        for product in products:
            dtos.append(ProductDTO(title=product.title, category_id=product.category_id, description=product.description, tags=product.tags.split(','), id=product.id))
        return dtos

    def get(self, id) -> Optional[ProductDTO]:
        product = self.session.query(ProductModel).where(ProductModel.id == id).first()
        if product is None:
            raise Exception(f"Product having ID: {id} does not exist")
        dto = ProductDTO(title=product.title, category_id=product.category_id, description=product.description, tags=product.tags.split(','), id=product.id)
        return dto

    def modify(self, payload: ProductDTO) -> ProductDTO:
        product_proxy = self.session.query(ProductModel).filter(ProductModel.id == payload.id)
        if product_proxy.first() is None:
            raise Exception(f"Product having ID: {payload.id} does not exist")
        payload.tags = ",".join([t.strip() for t in payload.tags])
        product_proxy.update(payload.model_dump(exclude_none=True), synchronize_session=False)
        self.session.commit()
        return payload



class PurchaseRepository():
    def __init__(self, session:Session) -> None:
        self.session = session
    
    def add(self, payload: PurchaseCreateDTO) -> PurchaseDTO:
        purchase = PurchaseModel(**payload.model_dump())
        
        customer_info = CustomerSVCUtils.fetch_customer_info(payload.customer_id)
        customer_id = customer_info["id"]
        customer_title = customer_info["title"]
        
        self.session.add(purchase)
        self.session.commit()
        self.session.refresh(purchase)
        
        product_dto = ProductRepository(self.session).get(purchase.product_id)
        category_dto = CategoryRepository(self.session).get(purchase.category_id)
        return PurchaseDTO(id=purchase.id, 
                           customer_id=customer_id, product_id=purchase.product_id, category_id=purchase.category_id,
                           customer_title=customer_title, product_title=product_dto.title, category_title=category_dto.title,
                           product_tags=product_dto.tags)



    def get(self, id) -> Optional[PurchaseDTO]:
        purchase = self.session.query(PurchaseModel).where(PurchaseModel.id == id).first()
        if purchase is None:
            raise Exception(f"Purchase having ID: {id} does not exist")
        
        customer_info = CustomerSVCUtils.fetch_customer_info(purchase.customer_id)
        customer_id = customer_info["id"]
        customer_title = customer_info["title"]
        
        product_dto = ProductRepository(self.session).get(purchase.product_id)
        category_dto = CategoryRepository(self.session).get(purchase.category_id)
        return PurchaseDTO(id=purchase.id, 
                           customer_id=customer_id, product_id=purchase.product_id, category_id=purchase.category_id,
                           customer_title=customer_title, product_title=product_dto.title, category_title=category_dto.title,
                           product_tags=product_dto.tags)
    
    def get_customer_purchases(self, customer_id) -> CustomerPurchaseCollectionDTO:
        customer_info = CustomerSVCUtils.fetch_customer_info(customer_id)
        
        purchases = self.session.query(PurchaseModel).where(PurchaseModel.customer_id == customer_id).limit(10).all()
        if purchases is None or len(purchases) < 1:
            return []
        
        purchase_IDvsCatProdIDs = dict([(p.__dict__['id'],(p.__dict__['category_id'],p.__dict__['product_id'])) for p in purchases])
        product_ids = set([p.product_id for p in purchases])
        category_ids = set([p.category_id for p in purchases])
        
        
        repo_category = CategoryRepository(self.session)
        categories = repo_category.get_all(ids=list(category_ids))
        category_IDvsTITLE = dict([(c.__dict__['id'],c.__dict__['title']) for c in categories])

        repo_product = ProductRepository(self.session)
        products = repo_product.get_all(ids=list(product_ids))
        product_IDvsInfo = dict([(p.__dict__['id'],(p.__dict__['title'], p.__dict__['tags'])) for p in products])

        purchase_record_dtos:List[CustomerPurchaseRecordDTO] = list()
        for k,v in purchase_IDvsCatProdIDs.items():
            dto = CustomerPurchaseRecordDTO(purchase_id=k, 
                                            category_id=v[0], category_title=category_IDvsTITLE[v[0]],
                                            product_id=v[1],  product_title=product_IDvsInfo[v[1]][0],
                                            product_tags=product_IDvsInfo[v[1]][1])
            purchase_record_dtos.append(dto)
        cpcdto = CustomerPurchaseCollectionDTO(id=customer_info["id"], title=customer_info["title"], 
                                               gender=customer_info["gender"], age=customer_info["age"], 
                                               location=customer_info["location"], preference=customer_info["preference"],
                                               purchases=purchase_record_dtos)
        return cpcdto
