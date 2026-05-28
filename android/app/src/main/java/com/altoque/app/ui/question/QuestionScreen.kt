package com.altoque.app.ui.question

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.altoque.app.ui.AppViewModel
import java.time.Instant

private val EMOJIS = listOf("😡", "😞", "😐", "🙂", "😍")

@Composable
fun QuestionScreen(navController: NavController, viewModel: AppViewModel) {
    val session = viewModel.currentSession ?: return

    fun submit(rating: Int?, action: String) {
        viewModel.setPendingResponse(rating, action, Instant.now().toString())
        navController.navigate("processing")
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceBetween,
    ) {
        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = session.question.text,
            style = MaterialTheme.typography.displaySmall,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth(),
        )

        // Botones de rating — mínimo 160dp de alto para tablet
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly,
        ) {
            EMOJIS.forEachIndexed { index, emoji ->
                val rating = index + 1
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .padding(horizontal = 8.dp)
                        .height(160.dp)
                        .clickable { submit(rating, "answered") },
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                    ) {
                        Text(emoji, fontSize = 56.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("$rating", style = MaterialTheme.typography.headlineMedium)
                    }
                }
            }
        }

        TextButton(
            onClick = { submit(null, "skipped") },
            modifier = Modifier.padding(bottom = 16.dp),
        ) {
            Text(
                "Omitir",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.outline,
            )
        }
    }
}
