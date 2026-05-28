package com.altoque.app.data.repository

import com.altoque.app.data.api.AlToqueApi
import com.altoque.app.data.api.ResponseOut
import com.altoque.app.data.api.ResponseRequest
import com.altoque.app.data.api.SessionStartResponse
import com.altoque.app.data.api.TableItem
import com.altoque.app.data.api.WaiterItem

class FeedbackRepository(private val api: AlToqueApi) {

    suspend fun getTables(restaurantId: String): List<TableItem> =
        api.getTables(restaurantId)

    suspend fun getWaiters(restaurantId: String): List<WaiterItem> =
        api.getWaiters(restaurantId)

    suspend fun startSession(
        restaurantId: String,
        tableId: String,
        waiterId: String,
    ): SessionStartResponse = api.startSession(restaurantId, tableId, waiterId)

    suspend fun postResponse(request: ResponseRequest): ResponseOut =
        api.postResponse(request)
}
