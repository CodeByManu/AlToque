package com.altoque.app.data.api

data class TableItem(val id: String, val number: Int)
data class WaiterItem(val id: String, val name: String)

data class QuestionItem(val id: String, val text: String, val category: String)

data class SessionStartResponse(
    val session_id: String,
    val question: QuestionItem,
    val shown_at: String,
)

data class ResponseRequest(
    val session_id: String,
    val question_id: String?,
    val rating: Int?,
    val action: String,
    val shown_at: String,
    val responded_at: String,
)

data class ResponseOut(
    val id: String,
    val action: String,
    val rating: Int?,
)
