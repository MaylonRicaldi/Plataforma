import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import App from './App'
import ErrorBoundary from './ErrorBoundary'
import { ToastProvider } from './ToastContext'

ReactDOM.createRoot(
document.getElementById('root')
).render(

<React.StrictMode>
<ErrorBoundary>
<ToastProvider>
<App/>
</ToastProvider>
</ErrorBoundary>
</React.StrictMode>

)