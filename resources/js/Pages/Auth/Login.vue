<template>
    <Head title="| Login"/>

    <!-- Login Form Container -->
    <div class="flex justify-center items-center min-h-screen bg-white-100 p-6">
        <div class="max-w-lg w-full bg-white p-8 rounded-lg shadow-lg">
            <h1 class="text-2xl font-bold text-gray-800 text-center mb-2">Welcome back!</h1>
            <p class="text-gray-600 text-center mb-6">Enter your credentials to access your account.</p>

            <!-- Login Form -->
            <form @submit.prevent="submit" class="space-y-4">
                <div class="mb-4">
                    <label class="block text-gray-700 mb-1">Email</label>
                    <div class="relative">
                        <InputText
                            type="email"
                            v-model="form.email"
                            placeholder="Enter your email"  
                            class="w-full h-12 pl-4 border rounded-lg"
                            :class="{'p-invalid': form.errors.email}"
                        />
                    </div>
                    <small class="text-red-500" v-if="form.errors.email">{{ form.errors.email }}</small>
                </div>

                <div class="mb-4">
                    <label class="block text-gray-700 mb-1">Password</label>
                    <div class="relative">
                        <Password
                            v-model="form.password"
                            placeholder="Enter your password"
                            :feedback="false"
                            :toggleMask="true"
                            class="w-full"
                            :inputClass="{'p-invalid': form.errors.password}"
                        />
                    </div>
                    <small class="text-red-500" v-if="form.errors.password">{{ form.errors.password }}</small>
                </div>

                <!-- Remember Me & Forgot Password -->
                <div class="flex justify-between items-center mb-6">
                    <div class="flex items-center">
                        <Checkbox v-model="form.remember" :binary="true" class="mr-2" />
                        <label class="text-gray-700 select-none cursor-pointer">Remember me</label>
                    </div>
                    <a href="#" class="text-blue-600 hover:underline">Forgot Password?</a>
                </div>

                <!-- Login Button -->
                <Button
                    type="submit"
                    label="Login"
                    :loading="form.processing"
                    class="w-full h-12 text-lg font-semibold bg-green-500 border-none text-white rounded-lg"
                />
            </form>
        </div>
    </div>
</template>

<script setup>
import { useForm } from '@inertiajs/vue3';
import { Head } from '@inertiajs/vue3';
import AuthLayout from '../../Layouts/AuthLayout.vue';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';

const form = useForm({
    email: '',
    password: '',
    remember: false
});

const submit = () => {
    form.clearErrors();

    let hasError = false;
    if (!form.email) {
        form.setError('email', 'Email is required');
        hasError = true;
    }
    if (!form.password) {
        form.setError('password', 'Password is required');
        hasError = true;
    }
    
    if (!hasError) {
        form.post(route('login'), {
            onError: (errors) => {
                console.error('Login failed:', errors);
                form.setError('email', 'Invalid email or password');
                form.reset('password');
            }
        });
    }
};

defineOptions({layout: AuthLayout});
</script>

<style scoped>
:deep(.p-password-input) {
    width: 100%;
    height: 3rem;
    padding-left: 1rem;
    border-radius: 0.5rem;
}

:deep(.p-password) {
    width: 100%;
}

:deep(.p-button) {
    background: #22c55e;
    border: none;
    border-radius: 0.5rem;
    color: white;
}

:deep(.p-button:hover) {
    background: #16a34a;
}

:deep(.p-inputtext) {
    width: 100%;
    padding-left: 1rem;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight) {
    background: #1B2850;
    border-color: #1B2850;
}

:deep(.p-password .p-inputtext.p-invalid) {
    border-color: #dc2626;
}
</style>