const { createApp } = Vue
const TaskApp = {
    data() {
        return {
            message: 'Hello, world!'
        }
    },
    delimiters: ['{', '}']
}

createApp(TaskApp).mount('#app')