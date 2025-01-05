from drf_spectacular.utils import extend_schema, extend_schema_view


workspace_offer_schema = extend_schema_view(

    list=extend_schema(
        tags=["Workspace -> Offer"],
        summary="Organization Offers List", 
    ),

    create=extend_schema(
        tags=["Workspace -> Offer"],
        summary="Create Offers for Users", 
    ),

    partial_update=extend_schema(
        tags=["Workspace -> Offer"],
        summary="Partially Update User Offer",
    ),
)


user_offer_schema = extend_schema_view(

    list=extend_schema(
        tags=["User -> Offer"],
        summary="User Offers List", 
    ),

    partial_update=extend_schema(
        tags=["User -> Offer"],
        summary="Partially Update User Offer",
    ),

    retrieve=extend_schema(
        tags=["User -> Offer"],
        summary="Get User Offer", 
    ),
)
