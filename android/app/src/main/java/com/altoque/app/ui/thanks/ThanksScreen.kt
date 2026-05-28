package com.altoque.app.ui.thanks

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.altoque.app.ui.AppViewModel
import kotlinx.coroutines.delay

@Composable
fun ThanksScreen(navController: NavController, viewModel: AppViewModel) {
    BackHandler(enabled = true) { /* impide volver atrás */ }

    var secondsLeft by remember { mutableIntStateOf(5) }

    LaunchedEffect(Unit) {
        repeat(5) {
            delay(1_000)
            secondsLeft--
        }
        viewModel.resetForNextCustomer()
        navController.navigate("setup") {
            popUpTo(0) { inclusive = true }
        }
    }

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text(
            text = "¡Gracias!",
            style = MaterialTheme.typography.displayLarge,
            color = MaterialTheme.colorScheme.primary,
        )

        Spacer(modifier = Modifier.height(40.dp))

        // Placeholder QR — se reemplaza en D7
        Box(
            modifier = Modifier
                .size(200.dp)
                .border(2.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(12.dp)),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = "QR próximamente",
                style = MaterialTheme.typography.bodyLarge,
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.outline,
            )
        }

        Spacer(modifier = Modifier.height(32.dp))

        Text(
            text = "Volviendo en $secondsLeft segundo${if (secondsLeft != 1) "s" else ""}...",
            style = MaterialTheme.typography.titleLarge,
            color = MaterialTheme.colorScheme.secondary,
        )
    }
}
