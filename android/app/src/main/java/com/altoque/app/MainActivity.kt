package com.altoque.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import com.altoque.app.ui.AppViewModel
import com.altoque.app.ui.navigation.AppNavigation
import com.altoque.app.ui.theme.AlToqueTheme

class MainActivity : ComponentActivity() {

    private val viewModel: AppViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AlToqueTheme {
                AppNavigation(viewModel = viewModel)
            }
        }
    }
}
