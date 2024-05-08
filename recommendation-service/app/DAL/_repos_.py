from typing import Optional, List

from common import ConfigVars, VectorUtils, MilvusUtils
from ._dtos_ import ProductInfoDTO, CustomerPurchaseCollectionDTO, CustomerPurchaseRecordDTO, RecommendationResultDTO



class RecommendationRepository():
    def __init__(self) -> None:
        pass

    def upsert_user(self, payload: CustomerPurchaseCollectionDTO):
        all_tags = set()
        all_products = set()
        all_categories = set()
        
        for p in payload.purchases:
            all_products.add(p.product_title.lower().strip())
            all_categories.add(p.category_title.lower().strip())
            curr_tags = [tag.lower().strip() for tag in p.product_tags]
            all_tags.update(curr_tags)
        
        all_tags = list(all_tags)
        all_products = list(all_products)
        all_categories = list(all_categories)
        
        all_tags.sort()
        all_products.sort()
        all_categories.sort()
        
        all_tags = ",".join([t for t in all_tags])
        all_products = ",".join([p for p in all_products])
        all_categories = ",".join([c for c in all_categories])
        
        vec_str = f"{payload.age},{payload.gender.lower().strip()},{payload.location.lower().strip()},{payload.preference.lower().strip()},{all_categories},{all_products},{all_tags}"
        vec_data = VectorUtils.text_to_vector(vec_str, True)
        
        entity_milvus = MilvusUtils.prepare_record_user_collection(payload.id, "", vec_str, vec_data)
        
        collection = MilvusUtils.get_collection(ConfigVars.MILVUS_COL_USERS)
        res = collection.upsert(entity_milvus, timeout=30)
        if res.upsert_count != 1:
            raise Exception("Error occured while performing user vectorizing operation")
    
    def upsert_product(self, payload: ProductInfoDTO):
        tags_list = [tag.lower().strip() for tag in payload.product_tags]
        tags_list.sort()
        tags_str = ",".join([t for t in tags_list])
        
        vec_str = f"{payload.category_title.lower().strip()},{payload.product_title.lower().strip()},{tags_str}"
        vec_data = VectorUtils.text_to_vector(vec_str, True)
        
        entity_milvus = MilvusUtils.prepare_record_prod_collection(payload.product_id, payload.category_id, payload.product_title, payload.category_title, vec_str, vec_data)
        
        collection = MilvusUtils.get_collection(ConfigVars.MILVUS_COL_PRODS)
        res = collection.upsert(entity_milvus, timeout=30)
        if res.upsert_count != 1:
            raise Exception("Error occured while performing product vectorizing operation")

    def get_recommendations(self, cpcdto:CustomerPurchaseCollectionDTO) -> List[RecommendationResultDTO]:
        
        # Refresh Customer Vector
        self.upsert_user(cpcdto)
        
        collection_user = MilvusUtils.get_collection(ConfigVars.MILVUS_COL_USERS)
        res_user = collection_user.query(expr = f"id == {cpcdto.id}", output_fields = ["vec_data"])
        if not len(res_user):
            raise Exception(f"Customer having ID: {cpcdto.id} does not exist")
        user_vector = res_user[0]["vec_data"]
        
        collection_prod = MilvusUtils.get_collection(ConfigVars.MILVUS_COL_PRODS)
        res = collection_prod.search(
            data=[user_vector], 
            anns_field="vec_data", 
            param={
                "metric_type": "IP", 
                "offset": 0, 
                "ignore_growing": False, 
                "params": {"nprobe": 10}
            },
            limit=10,
            expr=None,
            output_fields=['category_id', 'category_title', 'product_id', 'product_title'],
            consistency_level="Strong"
        )
        if not len(res):
            return []
        
        recommendations = []
        for hit in res[0]:
            rrdto = RecommendationResultDTO(category_id=hit.entity.get("category_id"), category=hit.entity.get("category_title"), 
                                            product_id=hit.entity.get("product_id"), product=hit.entity.get("product_title"))
            recommendations.append(rrdto)
        return recommendations
