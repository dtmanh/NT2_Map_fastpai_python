def register_routes(app, root="api"):
    from .user_controller import router as user_router
    from .auth_controller import router as auth_router
    from .system_logs_controller import router as system_logs_router
    from .role_controller import router as role_router
    from .system_configs_controller import router as system_configs_router
    from .minio_controller import router as minio_router
    from .permission_controller import router as permission_router
    from .satellite_controller import router as satellite_router
    from .mark_map_area_controller import router as mark_map_router
    # from .object_profile_controller import router as object_profile_router
    from .user_layer_controller import router as user_layer_router
    from .object_layer_controller import router as object_layer_router
    from .object_controller import router as object_router
    from .equipments_controller import router as equipment_router
    from .object_equipments_controller import router as object_equipment_router
    from .source_data_collection_controller import router as source_data_collection_router
    from .robot_source_data_collection_controller import router as robot_source_data_collection_router


    app.include_router(user_router, prefix=f"/{root}")
    app.include_router(auth_router, prefix=f"/{root}")
    app.include_router(system_logs_router, prefix=f"/{root}")
    app.include_router(role_router, prefix=f"/{root}")
    app.include_router(system_configs_router, prefix=f"/{root}")
    app.include_router(minio_router, prefix=f"/{root}")
    app.include_router(permission_router, prefix=f"/{root}")
    app.include_router(satellite_router, prefix=f"/{root}")
    app.include_router(mark_map_router, prefix=f"/{root}")
    # app.include_router(object_profile_router, prefix=f"/{root}")
    app.include_router(user_layer_router, prefix=f"/{root}")
    app.include_router(object_layer_router, prefix=f"/{root}")
    app.include_router(object_router, prefix=f"/{root}")
    app.include_router(equipment_router, prefix=f"/{root}")
    app.include_router(object_equipment_router, prefix=f"/{root}")
    app.include_router(source_data_collection_router, prefix=f"/{root}")
    app.include_router(robot_source_data_collection_router, prefix=f"/{root}")

