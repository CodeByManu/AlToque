package com.altoque.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val ColorScheme = lightColorScheme(
    primary = Color(0xFFE65100),
    onPrimary = Color.White,
    secondary = Color(0xFFFF8F00),
    background = Color(0xFFFAFAFA),
    surface = Color.White,
    outline = Color(0xFFBDBDBD),
)

@Composable
fun AlToqueTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = ColorScheme,
        content = content,
    )
}
