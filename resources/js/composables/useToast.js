import { useToast as usePrimeToast } from 'primevue/usetoast';

export function useToast() {
    const toast = usePrimeToast();

    const showSuccess = (message, title = 'Success') => {
        toast.add({
            severity: 'success',
            summary: title,
            detail: message,
            life: 3000
        });
    };

    const showError = (message, title = 'Error') => {
        toast.add({
            severity: 'error',
            summary: title,
            detail: message,
            life: 4000
        });
    };

    const showInfo = (message, title = 'DigiPort') => {
        toast.add({
            severity: 'info',
            summary: title,
            detail: message,
            life: 3000
        });
    };

    const showWarning = (message, title = 'Warning') => {
        toast.add({
            severity: 'warn',
            summary: title,
            detail: message,
            life: 3500
        });
    };

    return {
        showSuccess,
        showError,
        showInfo,
        showWarning
    };
}
