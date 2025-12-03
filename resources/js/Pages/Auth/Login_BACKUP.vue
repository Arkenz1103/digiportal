<template>
    <!-- Professional Login/Signup Page with Smooth Animations -->
    <div class="min-h-screen relative overflow-hidden bg-gray-900">
        <!-- Animated Dark Background -->
        <div class="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
            <!-- Animated Gradient Blobs -->
            <div class="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
            <div class="absolute top-1/2 right-0 w-96 h-96 bg-gradient-to-br from-orange-400/20 to-orange-600/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
            <div class="absolute bottom-0 left-1/3 w-96 h-96 bg-gradient-to-br from-red-500/20 to-orange-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
        </div>

        <!-- Back Button -->
        <button
            @click="goToLanding"
            class="absolute top-6 left-6 flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-lg text-white hover:bg-white/20 transition-all duration-200 font-medium shadow-lg z-20 border border-white/20"
        >
            <i class="pi pi-arrow-left"></i>
            <span class="hidden sm:inline">Back</span>
        </button>

        <!-- Main Container - Full Screen Design -->
        <div class="relative z-10 min-h-screen flex items-center justify-center overflow-hidden">
            <!-- Full Screen Layout with Directional Animation -->
            <transition
                :name="isLoginMode ? 'slide-login' : 'slide-signup'"
                mode="out-in"
            >
                <div
                    :key="isLoginMode ? 'login-layout' : 'signup-layout'"
                    class="w-full h-screen flex items-center justify-center relative"
                >

                    <!-- Left Side - Form (Login) or Welcome (Signup) -->
                    <div class="relative">
                        <!-- LOGIN FORM - Left Side -->
                        <div
                            v-if="isLoginMode"
                            class="relative bg-gray-800/40 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-8 md:p-10 shadow-2xl overflow-hidden"
                        >
                                <!-- Gradient Overlay -->
                                <div class="absolute inset-0 bg-gradient-to-br from-orange-600/5 to-transparent pointer-events-none"></div>

                                <!-- Content -->
                                <div class="relative z-10">
                                <!-- Form Title with Animation -->
                                <transition name="fade-slide" mode="out-in">
                                    <div :key="isLoginMode ? 'login' : 'signup'">
                                        <h2 class="text-3xl md:text-4xl font-bold text-white mb-2">
                                            {{ isLoginMode ? 'Login' : 'Register' }}
                                        </h2>
                                        <p class="text-gray-400 text-sm mb-8">
                                            {{ isLoginMode ? 'Welcome back to your portfolio' : 'Create your account to get started' }}
                                        </p>
                                    </div>
                                </transition>

                                <!-- Form with Transition -->
                                <form @submit.prevent="submitForm" class="space-y-5 form-animate">

                                    <!-- Role Selection (visible in both modes) -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-3">
                                            Select Role
                                        </label>
                                        <div class="grid grid-cols-2 gap-3">
                                            <button
                                                type="button"
                                                @click="form.role = 'teacher'"
                                                :class="[
                                                    'py-3 px-4 rounded-lg border-2 transition-all duration-300 font-medium',
                                                    form.role === 'teacher'
                                                        ? 'border-orange-500 bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-lg shadow-orange-500/50'
                                                        : 'border-gray-600 bg-gray-700/50 hover:bg-gray-700 text-gray-300'
                                                ]"
                                            >
                                                <i class="pi pi-user mr-2"></i>
                                                Teacher
                                            </button>
                                            <button
                                                type="button"
                                                @click="form.role = 'student'"
                                                :class="[
                                                    'py-3 px-4 rounded-lg border-2 transition-all duration-300 font-medium',
                                                    form.role === 'student'
                                                        ? 'border-orange-500 bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-lg shadow-orange-500/50'
                                                        : 'border-gray-600 bg-gray-700/50 hover:bg-gray-700 text-gray-300'
                                                ]"
                                            >
                                                <i class="pi pi-users mr-2"></i>
                                                Student
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.role">
                                            {{ form.errors.role }}
                                        </small>
                                    </div>

                                    <!-- Name Field (Signup only) -->
                                    <div v-if="!isLoginMode" class="form-field-stagger form-field-enter">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Full Name
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-user absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                type="text"
                                                v-model="form.name"
                                                class="w-full pl-10 pr-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your full name"
                                            />
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.name">
                                            {{ form.errors.name }}
                                        </small>
                                    </div>

                                    <!-- Email -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Email Address
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-envelope absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                type="email"
                                                v-model="form.email"
                                                class="w-full pl-10 pr-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your email"
                                            />
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.email">
                                            {{ form.errors.email }}
                                        </small>
                                    </div>

                                    <!-- Password -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Password
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                :type="showPassword ? 'text' : 'password'"
                                                v-model="form.password"
                                                class="w-full pl-10 pr-12 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your password"
                                            />
                                            <button
                                                type="button"
                                                @click="showPassword = !showPassword"
                                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-orange-500 transition-colors duration-200"
                                            >
                                                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.password">
                                            {{ form.errors.password }}
                                        </small>
                                    </div>

                                    <!-- Confirm Password (Signup only) -->
                                    <div v-if="!isLoginMode" class="form-field-stagger form-field-enter">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Confirm Password
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                :type="showConfirmPassword ? 'text' : 'password'"
                                                v-model="form.confirmPassword"
                                                class="w-full pl-10 pr-12 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Confirm your password"
                                            />
                                            <button
                                                type="button"
                                                @click="showConfirmPassword = !showConfirmPassword"
                                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-orange-500 transition-colors duration-200"
                                            >
                                                <i :class="showConfirmPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.confirmPassword">
                                            {{ form.errors.confirmPassword }}
                                        </small>
                                    </div>

                                    <!-- Remember Me (Login only) -->
                                    <div v-if="isLoginMode" class="form-field-stagger flex items-center justify-between">
                                        <label class="flex items-center gap-2 cursor-pointer">
                                            <input
                                                type="checkbox"
                                                v-model="form.remember"
                                                class="w-4 h-4 bg-gray-700 border border-gray-600 rounded cursor-pointer accent-orange-500"
                                            />
                                            <span class="text-sm text-gray-400">Remember me</span>
                                        </label>
                                        <a href="#" class="text-sm text-orange-500 hover:text-orange-400 transition-colors duration-200">
                                            Forgot password?
                                        </a>
                                    </div>

                                    <!-- Submit Button -->
                                    <button
                                        type="submit"
                                        :disabled="form.processing"
                                        class="form-field-stagger w-full py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white font-semibold rounded-lg hover:from-orange-700 hover:to-red-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:shadow-orange-500/50 transform hover:-translate-y-0.5 mt-6"
                                    >
                                        <span v-if="!form.processing" class="flex items-center justify-center gap-2">
                                            <i :class="isLoginMode ? 'pi pi-sign-in' : 'pi pi-user-plus'"></i>
                                            {{ isLoginMode ? 'Sign In' : 'Create Account' }}
                                        </span>
                                        <span v-else class="flex items-center justify-center gap-2">
                                            <i class="pi pi-spin pi-spinner"></i>
                                            {{ isLoginMode ? 'Signing in...' : 'Creating account...' }}
                                        </span>
                                    </button>
                                </form>

                                <!-- Toggle Form Mode -->
                                <p class="text-center text-gray-400 text-sm mt-6 form-field-stagger">
                                    {{ isLoginMode ? "Don't have an account?" : 'Already have an account?' }}
                                    <button
                                        type="button"
                                        @click="toggleFormMode"
                                        class="text-orange-500 hover:text-orange-400 font-semibold transition-colors duration-200 hover:scale-105 transform"
                                    >
                                        {{ isLoginMode ? 'Sign Up' : 'Sign In' }}
                                    </button>
                                </p>
                            </div>
                        </div>

                        <!-- WELCOME MESSAGE - Left Side (Signup Mode) -->
                        <div
                            v-else
                            class="hidden lg:flex flex-col justify-center items-center text-center lg:text-left welcome-animate"
                        >
                            <div class="relative">
                                <div class="relative bg-gradient-to-br from-orange-600/20 to-red-600/20 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-8 md:p-10 shadow-2xl welcome-card-animate">
                                    <div class="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-orange-500/30 to-transparent rounded-full filter blur-3xl -z-10"></div>
                                    <h3 class="text-3xl md:text-4xl font-bold text-white mb-4">WELCOME!</h3>
                                    <p class="text-gray-300 text-base leading-relaxed mb-6">We are delighted to have you here. If you need any assistance, feel free to reach out.</p>
                                    <div class="space-y-3 mt-8">
                                        <div class="flex items-center gap-3">
                                            <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                            <span class="text-gray-300 text-sm">Digital Portfolio Management</span>
                                        </div>
                                        <div class="flex items-center gap-3">
                                            <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                            <span class="text-gray-300 text-sm">Student Activity Tracking</span>
                                        </div>
                                        <div class="flex items-center gap-3">
                                            <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                            <span class="text-gray-300 text-sm">Secure & Professional</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Side - Welcome (Login) or Form (Signup) -->
                    <div class="relative">
                        <!-- WELCOME MESSAGE - Right Side (Login Mode) -->
                        <div
                            v-if="isLoginMode"
                            class="hidden lg:flex flex-col justify-center items-center text-center lg:text-left welcome-animate"
                        >
                        <div class="relative">
                            <!-- Welcome Card -->
                            <div class="relative bg-gradient-to-br from-orange-600/20 to-red-600/20 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-8 md:p-10 shadow-2xl welcome-card-animate">
                                <!-- Diagonal Accent -->
                                <div class="absolute top-0 right-0 w-40 h-40 bg-gradient-to-br from-orange-500/30 to-transparent rounded-full filter blur-3xl -z-10"></div>

                                <h3 class="text-3xl md:text-4xl font-bold text-white mb-4">
                                    {{ isLoginMode ? 'WELCOME BACK!' : 'WELCOME!' }}
                                </h3>
                                <p class="text-gray-300 text-base leading-relaxed mb-6">
                                    {{ isLoginMode
                                        ? 'We are happy to have you with us again. If you need anything, we are here to help.'
                                        : 'We are delighted to have you here. If you need any assistance, feel free to reach out.'
                                    }}
                                </p>

                                <!-- Features List -->
                                <div class="space-y-3 mt-8">
                                    <div class="flex items-center gap-3">
                                        <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                        <span class="text-gray-300 text-sm">Digital Portfolio Management</span>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                        <span class="text-gray-300 text-sm">Student Activity Tracking</span>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                        <span class="text-gray-300 text-sm">Secure & Professional</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </div>

                        <!-- SIGNUP FORM - Right Side (Signup Mode) -->
                        <div
                            v-else
                            class="relative bg-gray-800/40 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-8 md:p-10 shadow-2xl overflow-hidden"
                        >
                            <!-- Gradient Overlay -->
                            <div class="absolute inset-0 bg-gradient-to-br from-orange-600/5 to-transparent pointer-events-none"></div>

                            <!-- Content -->
                            <div class="relative z-10">
                                <!-- Form Title with Animation -->
                                <transition name="fade-slide" mode="out-in">
                                    <div :key="isLoginMode ? 'login' : 'signup'">
                                        <h2 class="text-3xl md:text-4xl font-bold text-white mb-2">
                                            {{ isLoginMode ? 'Login' : 'Register' }}
                                        </h2>
                                        <p class="text-gray-400 text-sm mb-8">
                                            {{ isLoginMode ? 'Welcome back to your portfolio' : 'Create your account to get started' }}
                                        </p>
                                    </div>
                                </transition>

                                <!-- Form with Transition -->
                                <form @submit.prevent="submitForm" class="space-y-5 form-animate">

                                    <!-- Role Selection (visible in both modes) -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-3">
                                            Select Role
                                        </label>
                                        <div class="grid grid-cols-2 gap-3">
                                            <button
                                                type="button"
                                                @click="form.role = 'teacher'"
                                                :class="[
                                                    'py-3 px-4 rounded-lg border-2 transition-all duration-300 font-medium',
                                                    form.role === 'teacher'
                                                        ? 'border-orange-500 bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-lg shadow-orange-500/50'
                                                        : 'border-gray-600 bg-gray-700/50 hover:bg-gray-700 text-gray-300'
                                                ]"
                                            >
                                                <i class="pi pi-user mr-2"></i>
                                                Teacher
                                            </button>
                                            <button
                                                type="button"
                                                @click="form.role = 'student'"
                                                :class="[
                                                    'py-3 px-4 rounded-lg border-2 transition-all duration-300 font-medium',
                                                    form.role === 'student'
                                                        ? 'border-orange-500 bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-lg shadow-orange-500/50'
                                                        : 'border-gray-600 bg-gray-700/50 hover:bg-gray-700 text-gray-300'
                                                ]"
                                            >
                                                <i class="pi pi-users mr-2"></i>
                                                Student
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.role">
                                            {{ form.errors.role }}
                                        </small>
                                    </div>

                                    <!-- Name Field (Signup only) -->
                                    <div v-if="!isLoginMode" class="form-field-stagger form-field-enter">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Full Name
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-user absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                type="text"
                                                v-model="form.name"
                                                class="w-full pl-10 pr-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your full name"
                                            />
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.name">
                                            {{ form.errors.name }}
                                        </small>
                                    </div>

                                    <!-- Email -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Email Address
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-envelope absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                type="email"
                                                v-model="form.email"
                                                class="w-full pl-10 pr-4 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your email"
                                            />
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.email">
                                            {{ form.errors.email }}
                                        </small>
                                    </div>

                                    <!-- Password -->
                                    <div class="form-field-stagger">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Password
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                :type="showPassword ? 'text' : 'password'"
                                                v-model="form.password"
                                                class="w-full pl-10 pr-12 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Enter your password"
                                            />
                                            <button
                                                type="button"
                                                @click="showPassword = !showPassword"
                                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-orange-500 transition-colors"
                                            >
                                                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.password">
                                            {{ form.errors.password }}
                                        </small>
                                    </div>

                                    <!-- Confirm Password (Signup only) -->
                                    <div v-if="!isLoginMode" class="form-field-stagger form-field-enter">
                                        <label class="block text-gray-300 text-sm font-semibold mb-2">
                                            Confirm Password
                                        </label>
                                        <div class="relative">
                                            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-orange-500"></i>
                                            <input
                                                :type="showConfirmPassword ? 'text' : 'password'"
                                                v-model="form.confirmPassword"
                                                class="w-full pl-10 pr-12 py-3 bg-gray-700/50 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 focus:bg-gray-700 focus:ring-2 focus:ring-orange-500/30 transition-all duration-300 text-white placeholder-gray-500"
                                                placeholder="Confirm your password"
                                            />
                                            <button
                                                type="button"
                                                @click="showConfirmPassword = !showConfirmPassword"
                                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-orange-500 transition-colors"
                                            >
                                                <i :class="showConfirmPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                                            </button>
                                        </div>
                                        <small class="text-red-400 text-xs mt-1 block" v-if="form.errors.confirmPassword">
                                            {{ form.errors.confirmPassword }}
                                        </small>
                                    </div>

                                    <!-- Remember Me (Login only) -->
                                    <div v-if="isLoginMode" class="form-field-stagger flex items-center justify-between">
                                        <label class="flex items-center gap-2 cursor-pointer">
                                            <input
                                                type="checkbox"
                                                v-model="form.remember"
                                                class="w-4 h-4 bg-gray-700 border border-gray-600 rounded cursor-pointer accent-orange-500"
                                            />
                                            <span class="text-sm text-gray-400">Remember me</span>
                                        </label>
                                        <a href="#" class="text-sm text-orange-500 hover:text-orange-400 transition-colors duration-200">
                                            Forgot password?
                                        </a>
                                    </div>

                                    <!-- Submit Button -->
                                    <button
                                        type="submit"
                                        :disabled="form.processing"
                                        class="form-field-stagger w-full py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white font-semibold rounded-lg hover:from-orange-700 hover:to-red-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:shadow-orange-500/50 transform hover:-translate-y-0.5 mt-6"
                                    >
                                        <span v-if="!form.processing" class="flex items-center justify-center gap-2">
                                            <i :class="isLoginMode ? 'pi pi-sign-in' : 'pi pi-user-plus'"></i>
                                            {{ isLoginMode ? 'Sign In' : 'Create Account' }}
                                        </span>
                                        <span v-else class="flex items-center justify-center gap-2">
                                            <i class="pi pi-spin pi-spinner"></i>
                                            {{ isLoginMode ? 'Signing in...' : 'Creating account...' }}
                                        </span>
                                    </button>
                                </form>

                                <!-- Toggle Form Mode -->
                                <p class="text-center text-gray-400 text-sm mt-6 form-field-stagger">
                                    {{ isLoginMode ? "Don't have an account?" : 'Already have an account?' }}
                                    <button
                                        type="button"
                                        @click="toggleFormMode"
                                        class="text-orange-500 hover:text-orange-400 font-semibold transition-colors duration-200 hover:scale-105 transform"
                                    >
                                        {{ isLoginMode ? 'Sign Up' : 'Sign In' }}
                                    </button>
                                </p>
                            </div>
                        </div>
                    </div>
                    </div>
                </transition>
            </div>
        </div>

        <!-- Footer -->
        <div class="absolute bottom-6 left-0 right-0 text-center">
            <p class="text-gray-500 text-xs">
                © 2025 Naawan Central School. All rights reserved.
            </p>
        </div>
    </div>
</template>


<script setup>
import { ref, reactive } from 'vue';

// Define emits
const emit = defineEmits(['navigate']);

// Form mode toggle
const isLoginMode = ref(true);

// Show/hide password toggles
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const goToLanding = () => {
    emit('navigate', 'Landing');
};

// Toggle between login and signup modes
const toggleFormMode = () => {
    isLoginMode.value = !isLoginMode.value;
    form.errors = {};
    form.name = '';
    form.confirmPassword = '';
};

// Function to get CSRF token from cookie
const getCsrfToken = () => {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Form data
const form = reactive({
    role: '',
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    remember: false,
    processing: false,
    errors: {}
});

const submitForm = async () => {
    form.errors = {};

    let hasError = false;

    // Validate role
    if (!form.role) {
        form.errors.role = 'Please select your role';
        hasError = true;
    }

    // Validate email
    if (!form.email) {
        form.errors.email = 'Email is required';
        hasError = true;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        form.errors.email = 'Please enter a valid email';
        hasError = true;
    }

    // Validate password
    if (!form.password) {
        form.errors.password = 'Password is required';
        hasError = true;
    } else if (form.password.length < 6) {
        form.errors.password = 'Password must be at least 6 characters';
        hasError = true;
    }

    // Signup-specific validations
    if (!isLoginMode.value) {
        if (!form.name) {
            form.errors.name = 'Full name is required';
            hasError = true;
        }

        if (!form.confirmPassword) {
            form.errors.confirmPassword = 'Please confirm your password';
            hasError = true;
        } else if (form.password !== form.confirmPassword) {
            form.errors.confirmPassword = 'Passwords do not match';
            hasError = true;
        }
    }

    if (!hasError) {
        form.processing = true;

        try {
            const csrfToken = getCsrfToken();
            const endpoint = isLoginMode.value ? '/api/auth/login/' : '/api/auth/register/';

            const payload = isLoginMode.value
                ? {
                    email: form.email,
                    password: form.password,
                    role: form.role
                }
                : {
                    email: form.email,
                    password: form.password,
                    name: form.name,
                    role: form.role
                };

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Store user data in localStorage
                localStorage.setItem('digiportal_user_role', data.user.role);
                localStorage.setItem('digiportal_user_email', data.user.email);
                localStorage.setItem('digiportal_user_name', data.user.name || data.user.username);
                localStorage.setItem('digiportal_user_id', data.user.id);

                // Store authentication token if provided
                if (data.token) {
                    localStorage.setItem('digiportal_auth_token', data.token);
                }

                console.log('✅ Authentication successful');
                console.log('🍪 Cookies after auth:', document.cookie);

                // Dispatch custom event to notify MainLayout of user data change
                window.dispatchEvent(new Event('userDataChanged'));

                // Wait a moment to ensure session cookie is fully set
                await new Promise(resolve => setTimeout(resolve, 100));

                console.log('✅ Proceeding to navigation...');

                // Navigate based on role
                if (data.user.role === 'teacher') {
                    emit('navigate', 'TeacherHome');
                } else if (data.user.role === 'student') {
                    emit('navigate', 'StudentNewsfeed');
                } else {
                    emit('navigate', 'Landing');
                }
            } else {
                // Handle error
                if (data.errors) {
                    form.errors = data.errors;
                } else {
                    form.errors.email = data.error || 'Authentication failed. Please try again.';
                }
            }
        } catch (error) {
            console.error('Auth error:', error);
            form.errors.email = 'An error occurred. Please try again.';
        } finally {
            form.processing = false;
        }
    }
};
</script>

<style scoped>
/* Animated Blob Background */
@keyframes blob {
    0%, 100% {
        transform: translate(0px, 0px) scale(1) rotate(0deg);
    }
    33% {
        transform: translate(30px, -50px) scale(1.1) rotate(120deg);
    }
    66% {
        transform: translate(-20px, 20px) scale(0.9) rotate(240deg);
    }
}

.animate-blob {
    animation: blob 20s infinite ease-in-out;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

/* Form Field Enter Animation */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.form-field-enter {
    animation: slideInUp 0.5s ease-out forwards;
}

/* Smooth input focus animation */
@keyframes inputFocus {
    from {
        box-shadow: 0 0 0 0 rgba(249, 115, 22, 0);
    }
    to {
        box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.1);
    }
}

input:focus {
    animation: inputFocus 0.3s ease-out;
}

/* Button hover lift effect */
@keyframes buttonLift {
    from {
        transform: translateY(0);
    }
    to {
        transform: translateY(-2px);
    }
}

button[type="submit"]:not(:disabled):hover {
    animation: buttonLift 0.3s ease-out forwards;
}

/* Spinner animation */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.pi-spinner {
    animation: spin 1s linear infinite;
}

/* Input autofill styling */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px rgba(55, 65, 81, 0.5) inset !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Smooth transitions for all interactive elements */
input,
button,
a {
    transition: all 0.3s ease;
}

/* Custom checkbox styling */
input[type="checkbox"] {
    cursor: pointer;
}

input[type="checkbox"]:checked {
    background-color: #f97316;
    border-color: #f97316;
}

/* Form Animation */
.form-animate {
    animation: formSlideIn 0.6s ease-out;
}

@keyframes formSlideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Vue Transition: Fade and Slide */
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-slide-enter-from {
    opacity: 0;
    transform: translateX(20px);
}

.fade-slide-leave-to {
    opacity: 0;
    transform: translateX(-20px);
}

/* Layout Slide Animations - Login/Signup */
.slide-login-enter-active,
.slide-login-leave-active,
.slide-signup-enter-active,
.slide-signup-leave-active {
    transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Login Mode: Layout slides from left */
.slide-login-enter-from {
    opacity: 0;
    transform: translateX(-100%);
}

.slide-login-leave-to {
    opacity: 0;
    transform: translateX(100%);
}

/* Signup Mode: Layout slides from right */
.slide-signup-enter-from {
    opacity: 0;
    transform: translateX(100%);
}

.slide-signup-leave-to {
    opacity: 0;
    transform: translateX(-100%);
}

/* Form Field Stagger Animation */
.form-field-stagger {
    animation: fieldStagger 0.5s ease-out forwards;
    opacity: 0;
}

.form-field-stagger:nth-child(1) { animation-delay: 0.1s; }
.form-field-stagger:nth-child(2) { animation-delay: 0.2s; }
.form-field-stagger:nth-child(3) { animation-delay: 0.3s; }
.form-field-stagger:nth-child(4) { animation-delay: 0.4s; }
.form-field-stagger:nth-child(5) { animation-delay: 0.5s; }
.form-field-stagger:nth-child(6) { animation-delay: 0.6s; }

@keyframes fieldStagger {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Input Field Animation on Focus */
input:focus,
textarea:focus {
    animation: inputPulse 0.4s ease-out;
}

@keyframes inputPulse {
    0% {
        box-shadow: 0 0 0 0 rgba(249, 115, 22, 0.4);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(249, 115, 22, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(249, 115, 22, 0);
    }
}

/* Button Click Animation */
button[type="submit"]:active {
    animation: buttonPress 0.2s ease-out;
}

@keyframes buttonPress {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(0.98);
    }
    100% {
        transform: scale(1);
    }
}

/* Role Button Animation */
.role-button-animate {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.role-button-animate:hover {
    animation: roleButtonHover 0.3s ease-out;
}

@keyframes roleButtonHover {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-3px);
    }
    100% {
        transform: translateY(-2px);
    }
}

/* Welcome Section Animation */
.welcome-animate {
    animation: welcomeSlideIn 0.8s ease-out 0.2s both;
}

@keyframes welcomeSlideIn {
    from {
        opacity: 0;
        transform: translateX(40px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Welcome Card Animation */
.welcome-card-animate {
    animation: cardFloat 3s ease-in-out infinite;
}

@keyframes cardFloat {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* Welcome Text Animation */
.welcome-animate h3 {
    animation: textFadeIn 0.8s ease-out 0.4s both;
}

.welcome-animate p {
    animation: textFadeIn 0.8s ease-out 0.5s both;
}

@keyframes textFadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .grid {
        gap: 2rem;
    }
}

@media (max-width: 768px) {
    .grid {
        gap: 1.5rem;
    }
}

@media (max-width: 640px) {
    .animate-blob {
        width: 200px;
        height: 200px;
    }
}
</style>
