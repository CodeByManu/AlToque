package com.altoque.app.data.api

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface AlToqueApi {

    @GET("api/v1/tables")
    suspend fun getTables(@Query("restaurant_id") restaurantId: String): List<TableItem>

    @GET("api/v1/waiters")
    suspend fun getWaiters(@Query("restaurant_id") restaurantId: String): List<WaiterItem>

    @GET("api/v1/sessions/start")
    suspend fun startSession(
        @Query("restaurant_id") restaurantId: String,
        @Query("table_id") tableId: String,
        @Query("waiter_id") waiterId: String,
    ): SessionStartResponse

    @POST("api/v1/responses")
    suspend fun postResponse(@Body body: ResponseRequest): ResponseOut
}
