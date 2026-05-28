import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

val localProps = Properties().apply {
    val f = rootProject.file("local.properties")
    if (f.exists()) load(f.inputStream())
}

android {
    namespace = "com.altoque.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.altoque.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        buildConfigField(
            "String", "RESTAURANT_ID",
            "\"${localProps["RESTAURANT_ID"] ?: ""}\""
        )
    }

    buildTypes {
        debug {
            buildConfigField(
                "String", "API_BASE_URL",
                "\"${localProps["API_BASE_URL_DEBUG"] ?: "http://10.0.2.2:8000"}\""
            )
        }
        release {
            isMinifyEnabled = false
            buildConfigField(
                "String", "API_BASE_URL",
                "\"${localProps["API_BASE_URL_RELEASE"] ?: "https://altoque-api.up.railway.app"}\""
            )
        }
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.13"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }
}

dependencies {
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.ui.tooling.preview)
    implementation(libs.compose.material3)
    implementation(libs.activity.compose)
    implementation(libs.navigation.compose)
    implementation(libs.lifecycle.viewmodel.compose)
    implementation(libs.retrofit)
    implementation(libs.retrofit.gson)
    implementation(libs.okhttp.logging)
    implementation(libs.coroutines.android)

    debugImplementation(libs.compose.ui.tooling)
}
