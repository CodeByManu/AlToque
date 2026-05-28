package com.altoque.app.ui.setup

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.altoque.app.ui.AppViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SetupScreen(navController: NavController, viewModel: AppViewModel) {
    val tables = viewModel.tables
    val waiters = viewModel.waiters
    val loadError = viewModel.loadError
    val sessionLoading = viewModel.sessionLoading
    val sessionError = viewModel.sessionError

    var tablesExpanded by remember { mutableStateOf(false) }
    var waitersExpanded by remember { mutableStateOf(false) }

    val canClose = viewModel.selectedTable != null && viewModel.selectedWaiter != null && !sessionLoading

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(48.dp),
        contentAlignment = Alignment.Center,
    ) {
        when {
            loadError != null -> {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = loadError,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyLarge,
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { viewModel.loadSetupData() }) {
                        Text("Reintentar")
                    }
                }
            }

            tables.isEmpty() -> {
                CircularProgressIndicator(modifier = Modifier.size(48.dp))
            }

            else -> {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(24.dp),
                    modifier = Modifier.widthIn(max = 480.dp),
                ) {
                    Text(
                        text = "AlToque",
                        style = MaterialTheme.typography.displaySmall,
                        color = MaterialTheme.colorScheme.primary,
                    )

                    ExposedDropdownMenuBox(
                        expanded = tablesExpanded,
                        onExpandedChange = { tablesExpanded = it },
                    ) {
                        OutlinedTextField(
                            value = viewModel.selectedTable?.let { "Mesa ${it.number}" } ?: "Seleccionar mesa",
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Mesa") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = tablesExpanded) },
                            textStyle = MaterialTheme.typography.titleLarge,
                            modifier = Modifier
                                .menuAnchor()
                                .fillMaxWidth(),
                        )
                        ExposedDropdownMenu(
                            expanded = tablesExpanded,
                            onDismissRequest = { tablesExpanded = false },
                        ) {
                            tables.forEach { table ->
                                DropdownMenuItem(
                                    text = { Text("Mesa ${table.number}", style = MaterialTheme.typography.titleMedium) },
                                    onClick = {
                                        viewModel.selectedTable = table
                                        tablesExpanded = false
                                    },
                                )
                            }
                        }
                    }

                    ExposedDropdownMenuBox(
                        expanded = waitersExpanded,
                        onExpandedChange = { waitersExpanded = it },
                    ) {
                        OutlinedTextField(
                            value = viewModel.selectedWaiter?.name ?: "Seleccionar garzón",
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Garzón") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = waitersExpanded) },
                            textStyle = MaterialTheme.typography.titleLarge,
                            modifier = Modifier
                                .menuAnchor()
                                .fillMaxWidth(),
                        )
                        ExposedDropdownMenu(
                            expanded = waitersExpanded,
                            onDismissRequest = { waitersExpanded = false },
                        ) {
                            waiters.forEach { waiter ->
                                DropdownMenuItem(
                                    text = { Text(waiter.name, style = MaterialTheme.typography.titleMedium) },
                                    onClick = {
                                        viewModel.selectedWaiter = waiter
                                        waitersExpanded = false
                                    },
                                )
                            }
                        }
                    }

                    sessionError?.let {
                        Text(
                            text = it,
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodyMedium,
                        )
                    }

                    Button(
                        onClick = {
                            viewModel.closeTable {
                                navController.navigate("question")
                            }
                        },
                        enabled = canClose,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(64.dp),
                    ) {
                        if (sessionLoading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
                                color = MaterialTheme.colorScheme.onPrimary,
                            )
                        } else {
                            Text("Cerrar mesa", style = MaterialTheme.typography.titleLarge)
                        }
                    }
                }
            }
        }
    }
}
