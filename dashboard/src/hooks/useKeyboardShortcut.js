import { useEffect } from 'react';

/**
 * Custom hook for keyboard shortcuts
 * @param {string} key - The key to listen for
 * @param {function} callback - Function to call when key is pressed
 * @param {boolean} ctrl - Whether Ctrl must be held
 */
export const useKeyboardShortcut = (key, callback, ctrl = false) => {
    useEffect(() => {
        const handleKeyDown = (event) => {
            const keyMatch = event.key.toLowerCase() === key.toLowerCase();
            const ctrlMatch = ctrl ? event.ctrlKey : true;

            if (keyMatch && ctrlMatch) {
                event.preventDefault();
                callback();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [key, callback, ctrl]);
};

export default useKeyboardShortcut;
