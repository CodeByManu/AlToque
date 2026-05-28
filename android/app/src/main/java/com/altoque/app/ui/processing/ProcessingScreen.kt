package com.altoque.app.ui.processing

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.altoque.app.ui.AppViewModel
import kotlinx.coroutines.delay

@Composable
fun ProcessingScreen(navController: NavController, viewModel: AppViewModel) {
    BackHandler(enabled = true) { /* impide volver atrás durante el pago */ }

    val retryMessage = viewModel.responseRetryMessage
    val error = viewModel.responseError

    LaunchedEffect(Unit) {
        val startTime = System.currentTimeMillis()
        val success = viewModel.submitPendingResponse()
        val remaining = 3_000L - (System.currentTimeMillis() - startTime)
        if (remaining > 0) delay(remaining)
        if (success) {
            navController.navigate("thanks") {
                popUpTo("question") { inclusive = true }
            }
        }
        // Si hay error, la pantalla muestra el estado de error con botón de continuar
    }

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        if (error == null) {
            CircularProgressIndicator(modifier = Modifier.size(72.dp), strokeWidth = 6.dp)
            Spacer(modifier = Modifier.height(24.dp))
            Text("Procesando pago...", style = MaterialTheme.typography.headlineLarge)
            retryMessage?.let {
                Spacer(modifier = Modifier.height(12.dp))
                Text(it, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.secondary)
            }
        } else {
            Text("⚠️", style = MaterialTheme.typography.displayMedium)
            Spacer(modifier = Modifier.height(16.dp))
            Text(error, style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.error)
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = {
                    navController.navigate("thanks") {
                        popUpTo("question") { inclusive = true }
                    }
                },
                modifier = Modifier.height(56.dp),
            ) {
                Text("Continuar de todos modos", style = MaterialTheme.typography.titleMedium)
            }
        }
    }
}
