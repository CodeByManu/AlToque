package com.altoque.app.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.altoque.app.ui.AppViewModel
import com.altoque.app.ui.processing.ProcessingScreen
import com.altoque.app.ui.question.QuestionScreen
import com.altoque.app.ui.setup.SetupScreen
import com.altoque.app.ui.thanks.ThanksScreen

@Composable
fun AppNavigation(viewModel: AppViewModel) {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "setup") {
        composable("setup") {
            SetupScreen(navController = navController, viewModel = viewModel)
        }
        composable("question") {
            QuestionScreen(navController = navController, viewModel = viewModel)
        }
        composable("processing") {
            ProcessingScreen(navController = navController, viewModel = viewModel)
        }
        composable("thanks") {
            ThanksScreen(navController = navController, viewModel = viewModel)
        }
    }
}
