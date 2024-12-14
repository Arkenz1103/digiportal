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

    // Basic validation
    let hasError = false;

    if (!form.email) {
        form.setError('email', 'Username is required');
        hasError = true;
    }

    if (!form.password) {
        form.setError('password', 'Password is required');
        hasError = true;
    } else if (form.password.length < 6) {
        form.setError('password', 'Password must be at least 6 characters');
        hasError = true;
    }

    // Only submit if no errors
    if (!hasError) {
        form.post(route("login"), {
            onError: () => {
                form.setError('email', 'Invalid username or password');
                form.reset('password');
            }
        });
    }
};

defineOptions({layout: AuthLayout});
</script>

<template>
    <Head title="| Login"/>

    <!-- Login Form -->
    <form @submit.prevent="submit" class="space-y-4">
        <div class="mb-4">
            <div class="relative">
                <i class="pi pi-user absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 z-10"></i>
                <InputText
                    type="text"
                    v-model="form.email"
                    placeholder="Enter your username"
                    class="w-full h-12 pl-10 rounded-lg"
                    :class="{'p-invalid': form.errors.email}"
                />
            </div>
            <small class="text-red-500 mt-1 block" v-if="form.errors.email">{{ form.errors.email }}</small>
        </div>

        <div class="mb-4">
            <div class="relative">
                <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 z-10"></i>
                <Password
                    v-model="form.password"
                    placeholder="Enter your password"
                    :feedback="false"
                    :toggleMask="true"
                    class="w-full"
                    :inputClass="{'p-invalid': form.errors.password}"
                />
            </div>
            <small class="text-red-500 mt-1 block" v-if="form.errors.password">{{ form.errors.password }}</small>
        </div>

        <!-- Remember Me -->
        <div class="mb-6 flex items-center">
            <Checkbox v-model="form.remember" :binary="true" class="mr-2" />
            <label class="text-gray-700 select-none cursor-pointer">Remember me</label>
        </div>

        <Button
            type="submit"
            label="LOGIN"
            :loading="form.processing"
            class="w-full h-12 text-lg font-semibold"
        />
    </form>
</template>

<style scoped>
:deep(.p-password-input) {
    width: 100%;
    height: 3rem;
    padding-left: 2.5rem;
    border-radius: 0.5rem;
}

:deep(.p-password) {
    width: 100%;
}

:deep(.p-button) {
    background: #1B2850;
    border: none;
    border-radius: 0.5rem;
}

:deep(.p-button:hover) {
    background: #2a3d75;
}

:deep(.p-inputtext) {
    width: 100%;
    padding-left: 2.5rem;
}

/* Remove the bottom border from password input */
:deep(.p-password .p-inputtext) {
    border-bottom: none !important;
}

/* Ensure password toggle icon is properly positioned */
:deep(.p-password i.p-password-icon) {
    right: 0.75rem;
    color: #6b7280;
}

/* Style checkbox */
:deep(.p-checkbox) {
    width: 1.25rem;
    height: 1.25rem;
}

:deep(.p-checkbox .p-checkbox-box.p-highlight) {
    background: #1B2850;
    border-color: #1B2850;
}

:deep(.p-password .p-inputtext.p-invalid) {
    border-color: #dc2626;
}
</style>
