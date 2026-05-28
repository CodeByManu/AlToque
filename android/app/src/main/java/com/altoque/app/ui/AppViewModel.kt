package com.altoque.app.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.altoque.app.BuildConfig
import com.altoque.app.data.api.ResponseRequest
import com.altoque.app.data.api.SessionStartResponse
import com.altoque.app.data.api.TableItem
import com.altoque.app.data.api.WaiterItem
import com.altoque.app.data.network.RetrofitClient
import com.altoque.app.data.repository.FeedbackRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class AppViewModel : ViewModel() {

    private val repository = FeedbackRepository(RetrofitClient.api)
    private val restaurantId = BuildConfig.RESTAURANT_ID

    // Setup data
    var tables by mutableStateOf<List<TableItem>>(emptyList())
        private set
    var waiters by mutableStateOf<List<WaiterItem>>(emptyList())
        private set
    var loadError by mutableStateOf<String?>(null)
        private set

    // Selección del garzón
    var selectedTable by mutableStateOf<TableItem?>(null)
    var selectedWaiter by mutableStateOf<WaiterItem?>(null)

    // Sesión activa
    var currentSession by mutableStateOf<SessionStartResponse?>(null)
        private set
    var sessionLoading by mutableStateOf(false)
        private set
    var sessionError by mutableStateOf<String?>(null)
        private set

    // Datos de la respuesta pendiente (seteados en QuestionScreen, consumidos en ProcessingScreen)
    private var pendingAction: String = ""
    private var pendingRating: Int? = null
    private var pendingRespondedAt: String = ""

    // Estado de envío de respuesta
    var responseRetryMessage by mutableStateOf<String?>(null)
        private set
    var responseError by mutableStateOf<String?>(null)
        private set

    init {
        loadSetupData()
    }

    fun loadSetupData() {
        loadError = null
        viewModelScope.launch {
            try {
                tables = repository.getTables(restaurantId)
                waiters = repository.getWaiters(restaurantId)
            } catch (e: Exception) {
                loadError = "No se pudo cargar datos del restaurante"
            }
        }
    }

    fun closeTable(onNavigate: () -> Unit) {
        val table = selectedTable ?: return
        val waiter = selectedWaiter ?: return
        viewModelScope.launch {
            sessionLoading = true
            sessionError = null
            try {
                currentSession = repository.startSession(restaurantId, table.id, waiter.id)
                sessionLoading = false
                onNavigate()
            } catch (e: Exception) {
                sessionError = "Error de conexión. Verificá la red."
                sessionLoading = false
            }
        }
    }

    fun setPendingResponse(rating: Int?, action: String, respondedAt: String) {
        pendingAction = action
        pendingRating = rating
        pendingRespondedAt = respondedAt
    }

    suspend fun submitPendingResponse(): Boolean {
        val session = currentSession ?: return true
        responseError = null

        val request = ResponseRequest(
            session_id = session.session_id,
            question_id = if (pendingAction == "answered") session.question.id else null,
            rating = pendingRating,
            action = pendingAction,
            shown_at = session.shown_at,
            responded_at = pendingRespondedAt,
        )

        // 3 intentos con backoff lineal (0s, 1s, 2s)
        repeat(3) { attempt ->
            if (attempt > 0) {
                responseRetryMessage = "Reintentando... (${attempt + 1}/3)"
                delay(1000L * attempt)
            }
            try {
                repository.postResponse(request)
                responseRetryMessage = null
                return true
            } catch (_: Exception) {
                // continúa al siguiente intento
            }
        }

        responseRetryMessage = null
        responseError = "No se pudo registrar la respuesta. Avise al garzón."
        return false
    }

    fun resetForNextCustomer() {
        currentSession = null
        pendingAction = ""
        pendingRating = null
        pendingRespondedAt = ""
        selectedTable = null
        selectedWaiter = null
        responseError = null
        responseRetryMessage = null
        sessionError = null
    }
}
